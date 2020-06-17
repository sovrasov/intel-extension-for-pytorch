import torch
import torch_ipex
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

cpu_device = torch.device("cpu")

##### upsample linear 1D #####
input_cpu = torch.randn((2,3,5), dtype=torch.float32, device = cpu_device)
input_dpcpp = input_cpu.to('dpcpp')
scales = [6]
input_cpu.requires_grad = True
input_dpcpp.requires_grad = True
alc = False #we don't support this path by currently as oneDNN don't support this algorithm! 
rsf = False

output_cpu = torch.nn.functional.interpolate(input_cpu, scale_factor=scales, mode='linear', align_corners=alc, recompute_scale_factor=rsf)
output_dpcpp = torch.nn.functional.interpolate(input_dpcpp, scale_factor=scales, mode='linear', align_corners=alc, recompute_scale_factor=rsf)
print("cpu result = ", output_cpu)
print("dpcpp result = ", output_dpcpp.cpu())
print("fwd result diff = ", output_cpu - output_dpcpp.cpu())

grad_out_cpu = torch.randn((2,3,30), dtype=torch.float32, device = cpu_device)
grad_out_dpcpp = grad_out_cpu.to("dpcpp")
grad_out_cpu = Variable(grad_out_cpu, requires_grad = True)
grad_out_dpcpp = Variable(grad_out_dpcpp, requires_grad = True)

output_cpu.backward(grad_out_cpu)
output_dpcpp.backward(grad_out_dpcpp)
grad_cpu = input_cpu.grad
grad_dpcpp = input_dpcpp.grad
print("x_cpu grad = ", grad_cpu)
print("x_dpcpp grad = ", grad_dpcpp.cpu())
print("bwd result diff = ", grad_cpu - grad_dpcpp.cpu())

##### upsample linear 2D #####
input_cpu = torch.randn((2,3,5,5), dtype=torch.float32, device = cpu_device)
input_dpcpp = input_cpu.to('dpcpp')
scales = [6, 8]
input_cpu.requires_grad = True
input_dpcpp.requires_grad = True
alc = False

output_cpu = torch.nn.functional.interpolate(input_cpu, scale_factor=scales, mode='bilinear', align_corners=alc, recompute_scale_factor=rsf)
output_dpcpp = torch.nn.functional.interpolate(input_dpcpp, scale_factor=scales, mode='bilinear', align_corners=alc, recompute_scale_factor=rsf)
print("cpu result = ", output_cpu)
print("dpcpp result = ", output_dpcpp.cpu())
print("fwd result diff = ", output_cpu - output_dpcpp.cpu())

grad_out_cpu = torch.randn((2,3,30,40), dtype=torch.float32, device = cpu_device)
grad_out_dpcpp = grad_out_cpu.to("dpcpp")
grad_out_cpu = Variable(grad_out_cpu, requires_grad = True)
grad_out_dpcpp = Variable(grad_out_dpcpp, requires_grad = True)

output_cpu.backward(grad_out_cpu)
output_dpcpp.backward(grad_out_dpcpp)
grad_cpu = input_cpu.grad
grad_dpcpp = input_dpcpp.grad
print("x_cpu grad = ", grad_cpu)
print("x_dpcpp grad = ", grad_dpcpp.cpu())
print("bwd result diff = ", grad_cpu - grad_dpcpp.cpu())

##### upsample linear 1D #####
input_cpu = torch.randn((2,3,2,5,5), dtype=torch.float32, device = cpu_device)
input_dpcpp = input_cpu.to('dpcpp')
scales = [6, 8, 1]
input_cpu.requires_grad = True
input_dpcpp.requires_grad = True
alc = False

output_cpu = torch.nn.functional.interpolate(input_cpu, scale_factor=scales, mode='trilinear', align_corners=alc, recompute_scale_factor=rsf)
output_dpcpp = torch.nn.functional.interpolate(input_dpcpp, scale_factor=scales, mode='trilinear', align_corners=alc, recompute_scale_factor=rsf)
print("cpu result = ", output_cpu)
print("dpcpp result = ", output_dpcpp.cpu())
print("fwd result diff = ", output_cpu - output_dpcpp.cpu())

grad_out_cpu = torch.randn((2,3,12,40,5), dtype=torch.float32, device = cpu_device)
grad_out_dpcpp = grad_out_cpu.to("dpcpp")
grad_out_cpu = Variable(grad_out_cpu, requires_grad = True)
grad_out_dpcpp = Variable(grad_out_dpcpp, requires_grad = True)

output_cpu.backward(grad_out_cpu)
output_dpcpp.backward(grad_out_dpcpp)
grad_cpu = input_cpu.grad
grad_dpcpp = input_dpcpp.grad
print("x_cpu grad = ", grad_cpu)
print("x_dpcpp grad = ", grad_dpcpp.cpu())
print("bwd result diff = ", grad_cpu - grad_dpcpp.cpu())
