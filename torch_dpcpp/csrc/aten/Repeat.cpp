#include <ATen/ATen.h>
#include <ATen/native/Repeat.h>
#include <c10/dpcpp/SYCLUtils.h>
#include <c10/dpcpp/SYCLMemory.h>

DP_DEF_K1(ComputeDpcppKer);

static void compute_dpcpp_kernel(int64_t *repeat_ptr, int64_t *cumsum_ptr, int64_t *result_ptr, int64_t size) {
  auto queue = c10::sycl::syclGetCurrentQueue();
  int64_t rng, grng, tile_size;
  c10::sycl::parallel_for_setup(size, tile_size, rng, grng);

  auto cgf = DP_Q_CGF(cgh) {
    auto rep_acc = c10::sycl::SYCLAccessor<dp_rw_mode>(cgh, repeat_ptr);
    auto cum_acc = c10::sycl::SYCLAccessor<dp_rw_mode>(cgh, cumsum_ptr);
    auto res_acc = c10::sycl::SYCLAccessor<dp_rw_mode>(cgh, result_ptr);

    auto kfn = DP_Q_KFN(DP::nd_item<1>item) {
      auto rep_ptr = rep_acc.template get_pointer<int64_t>();
      auto cum_ptr = cum_acc.template get_pointer<int64_t>();
      auto res_ptr = res_acc.template get_pointer<int64_t>();

      for (int64_t i = item.get_global_id(0); i < size; i += item.get_global_range()[0]) {
        int64_t end = cum_ptr[i];
        int64_t repeat = rep_ptr[i];
        int64_t start = end - repeat;
        for(int64_t j = start; j < end; j++) {
            res_ptr[j] = i;
        }
      }
    };
    // kick off kernel
    cgh.parallel_for<DP_K(ComputeDpcppKer)>(
      DP::nd_range<1>(DP::range<1>(grng), DP::range<1>(tile_size)), kfn);
  };

  DP_Q_ASYNC_SUBMIT(queue, cgf);
}

static void compute_dpcpp(int64_t *repeat_ptr, int64_t *cumsum_ptr, int64_t *result_ptr, int64_t size) {
    compute_dpcpp_kernel(repeat_ptr, cumsum_ptr, result_ptr, size);
}

namespace at { namespace native {

Tensor repeat_interleave_dpcpp(const Tensor &repeat) {
    return repeat_interleave_common<compute_dpcpp>(repeat);
}

}}
