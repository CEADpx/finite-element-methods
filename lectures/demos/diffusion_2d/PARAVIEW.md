# Inspecting the diffusion result in ParaView

Use the desktop ParaView application independently of the notebook's Python environment. This computer has ParaView 6.1.0. Finish the notebook first; keep `results/diffusion.xdmf` and `results/diffusion.h5` in the same directory.

1. Choose **File > Open**, select `diffusion.xdmf`, and click **Apply** in Properties. If asked for a reader, choose **Xdmf3ReaderS** (the XDMF3 reader); that reader was tested here. The automatically selected older reader did not expose the u field in this test. Do not open the HDF5 file by itself.
2. Select the loaded dataset in Pipeline Browser and press **Reset Camera**. Choose the view along the z axis so the square fills the view.
3. Set coloring to the point field **u**, then **Rescale to Data Range** and show the color legend. A single solid color usually means Solid Color is selected, not that the PDE solution is constant.
4. Choose **Surface With Edges** to see the triangular mesh. Label the field as a nondimensional diffusion variable; no temperature unit has been assigned in this example.
5. Compare the zero boundary and interior peak with the notebook image. Use the legend to interpret magnitudes. For this manufactured case, the exact maximum is one at the square's center; the discrete maximum approaches it with refinement.
6. Optionally choose **Plot Over Line**, with endpoints (0,0.5,0) and (1,0.5,0), and Apply. The exact section is sin(pi x). Use this as a shape check, not a replacement for the integrated error calculation.
7. Save a screenshot using **File > Save Screenshot**. A Warp By Scalar view is optional; it displays the scalar as height and is not a physical deformation of the domain.

If the field is absent, first check that the reader is Xdmf3ReaderS, enable the u array in its Properties, and Apply again. If the reader cannot find the heavy-data file, restore the `.h5` companion beside the `.xdmf`. If output was rewritten during a refinement experiment, reload the file before comparing.

[ParaView's data-loading documentation](https://docs.paraview.org/en/latest/UsersGuide/dataIngestion.html) describes Open, reader selection, and Apply. See VALIDATION.md for exactly which steps were executed in this run.
