#include <ATen/ATen.h>
#include <ATen/AccumulateType.h>
#include <ATen/dpcpp/SYCLContext.h>
#include <c10/dpcpp/SYCLMemory.h>
#include <c10/dpcpp/SYCLUtils.h>
#include <ATen/dpcpp/SYCLApplyUtils.h>

namespace at {
namespace sycl {
template <typename scalar_t, typename scalar1_t>
class where_functor {
 public:
  where_functor() {}
  void operator()(
      scalar_t& ret_val,
      const scalar1_t& cond_val,
      const scalar_t& self_val,
      const scalar_t& other_val) const {
    ret_val = cond_val ? self_val : other_val;
  }
};

} // namespace sycl
} // namespace at

namespace {
using namespace at;
using namespace at::sycl;
template <typename scalar_t>
void where_sycl(
    at::Tensor& ret,
    const at::Tensor& condition,
    const at::Tensor& self,
    const at::Tensor& other) {
  if (condition.scalar_type() == at::ScalarType::Byte) {
    SYCL_tensor_apply4<scalar_t, uint8_t, scalar_t, scalar_t>(
        ret, condition, self, other, where_functor<scalar_t, uint8_t>());
  } else {
    SYCL_tensor_apply4<scalar_t, bool, scalar_t, scalar_t>(
        ret, condition, self, other, where_functor<scalar_t, bool>());
  }
}
} // namespace

namespace at {
namespace native {
Tensor _s_where_sycl(
    const Tensor& condition,
    const Tensor& self,
    const Tensor& other) {
  Tensor ret = at::empty(self.sizes(), self.options());
  AT_DISPATCH_ALL_TYPES_AND2(at::ScalarType::Half, at::ScalarType::Bool, ret.scalar_type(), "where", [&] {
    where_sycl<scalar_t>(ret, condition, self, other);
  });
  return ret;
}

} // namespace native
} // namespace at
