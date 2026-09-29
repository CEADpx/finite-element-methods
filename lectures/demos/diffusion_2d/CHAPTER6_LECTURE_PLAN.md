# Chapter 6 in one 75-minute lecture

Aim: students should connect a 2D mesh and local basis to a physical gradient, an element equation, global assembly, prescribed values, and a computed field. Cover the chapter's overall construction; assign the detailed 3D/vector extensions as reading. Complete line-by-line treatment of the entire chapter plus a first software demo is not realistic in 75 minutes.

| Minutes | Content | Board or notebook action |
|---|---|---|
| 0–5 | Recall Chapter 5 construction and identify what changes in 2D | Mesh, local nodes, global DOFs; no repeat of full 1D assembly |
| 5–15 | P1 triangle and conformity | Reference basis 1-xi-eta, xi, eta; nodal property and shared-edge trace |
| 15–27 | Map to a physical triangle | x=x1+J[xi,eta]; grad(phi)=J^{-T}grad_hat(phi); integration Jacobian abs(det J); physical triangle area = abs(det J)/2 |
| 27–38 | Scalar diffusion element | K_ab = area*k*grad(phi_a) dot grad(phi_b) for constant k; show where quadrature replaces this expression for variable k |
| 38–44 | Assembly and boundary conditions | Local-to-global map, assembled system, prescribed values; recall rather than rederive Chapter 5 |
| 44–50 | Generalization | Q1 bilinear map; vector DOFs and elasticity; tetrahedra/hexahedra follow the same mapped-integration sequence |
| 50–66 | First FEniCSx demonstration | Problem, mesh, coefficient/source, boundary DOFs, forms, solve, plot, L2 error, export |
| 66–71 | ParaView and prediction | Display field/edges; ask what doubling conductivity with fixed source does |
| 71–75 | Questions and next chapter | Explain what was verified; assign energy error and refinement for follow-up |

## Six-minute triangle activity (inside minutes 15–27)

Use physical nodes (0,0), (2,0), (0,1). J=diag(2,1), abs(det J)=2, reference area=1/2, physical area=1. Ask students to transform grad_hat(phi1)=(-1,-1), grad_hat(phi2)=(1,0), grad_hat(phi3)=(0,1). Answers: (-1/2,-1), (1/2,0), (0,1). Their sum is zero. This checks the inverse transpose and prepares element integration without consuming a second full assembly example.

## Instructor element check (minutes 27–38)

For this triangle and k=1, K=[[1.25,-0.25,-1],[-0.25,0.25,0],[-1,0,1]]. It is symmetric and each row sums to zero. A single element has a constant null mode; essential boundary conditions remove the corresponding global ambiguity. For constant source f=1, F=[1/3,1/3,1/3]. State that these are element contributions, not a fully constrained global solve.

## Reading before/after class

Before: Chapter 6 sections on cells, scalar interpolation, and diffusion; recall Chapter 5 assembly. After: higher-order triangle details, quadrilateral numerical examples, 3D facet integration, tetrahedron/hexahedron numbering, and full elasticity/CST construction. These details remain in the book even though lecture concentrates on the common method.

## If class runs late

At minute 50 start the prepared notebook regardless of unfinished optional examples. Skip the energy-error cell and refinement discussion during class. If software startup fails, use the saved executed notebook and solution image, then explain the same visible code. Do not attempt package installation live. Preserve at least three minutes for questions. A quiz within this 75-minute block would require reducing the derivation segment explicitly.

## Before students arrive

Restart and run all on the teaching machine to populate the JIT cache, and keep the prepared kernel open. Pre-open the XDMF in ParaView with Xdmf3ReaderS. The conductivity question is a prediction only in class; the optional code experiment is for later. Saved notebook outputs are explicitly a prior verified run, not a live computation.
