*SOLUTION COMMENCED AT 14:11 ON 02/04/2026 
  
 Straus7 [R3.1.6][Solver Build R3.1.6] (64-Bit) [STUDENT VERSION - EDUCATIONAL USE ONLY] 
  
 LICENCED TO                 : Antonio Valeriano 
  
 ANALYSIS TYPE               : LINEAR STATIC 
  
 COMPUTER NAME               : MUFFIN 
 USER LOGON NAME             : frank 
 CPU                         : AMD Ryzen 7 5700U with Radeon Graphics  
 USABLE PHYSICAL MEMORY      : 15.3 GB 
 USABLE VIRTUAL MEMORY       : 17.6 GB 
  
 MODEL FILE                  : "C:\Users\frank\OneDrive\Desktop\Antonio\Università\2_MAGISTRALE\1 ANNO\femDEV\Optigeo2026\TestFE\Tet4\Tensione Monoassiale.st7" 
 RESULT FILE                 : "C:\Users\frank\OneDrive\Desktop\Antonio\Università\2_MAGISTRALE\1 ANNO\femDEV\Optigeo2026\TestFE\Tet4\Tensione Monoassiale.LSA" 
 SCRATCH PATH                : "C:\Users\frank\Straus7 R31\Tmp\" 
  
 TOTALS 
 Nodes                       : 4 
 Beams                       : 0 
 Plates                      : 0 
 Bricks                      : 1 
 Links                       : 0 
  
 SOLVER UNITS 
 Length                      : mm 
 Mass                        : t 
 Force                       : N 
 Stress                      : MPa 
  
 FREEDOM CASE                : "1:Freedom Case 1" 
  
 LOAD CASES                  : "1:Load Case 1" 
  
 STORAGE SCHEME              : Sparse  
 SORTING METHOD              : AMD  
 SOLUTION TYPE               : Direct  
  
 NUMBER OF EQUATIONS         : 3 
 MATRIX FILL-IN              : 0.0% 
 [K] MATRIX SIZE             : < 1 KB 
 OPTIMUM RAM NEEDED          : 128.0 KB 
 FREE SCRATCH SPACE          : 224.5 GB 
  
*WARNING[237]:Default freedom conditions might be over-constrained - one or more elements might require additional freedoms. 
  
 SUMMATION OF APPLIED LOADS  
          Case        FX           FY           FZ           MX           MY           MZ        Case Name 
 Nodes       1   +0.00000E+00 +0.00000E+00 +1.00000E+04 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
 Bricks      1   +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
 Total       1   +0.00000E+00 +0.00000E+00 +1.00000E+04 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
 Vector      1   +0.00000E+00 +0.00000E+00 +1.00000E+04 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
  
 SUMMATION OF MOMENTS OF APPLIED LOADS ABOUT THE ORIGIN [Vector]  
          Case        MXo          MYo          MZo       Case Name 
             1   +0.00000E+00 -1.00000E+07 +0.00000E+00   "1:Load Case 1" 
  
 Reducing 3 equations using 128.0 KB RAM for [K] of < 1 KB... 
  
 MAXIMUM PIVOT               : 4.000000E+07 (Node 1 DX) 
 MINIMUM PIVOT               : 3.333333E+07 (Node 4 DZ) 
  
 Results for 1 load case... 
  
 MAXIMUM NODE DISPLACEMENT MAGNITUDES 
   Case        DX           DY           DZ           RX           RY           RZ       Case Name 
      1    7.50000E-05  7.50000E-05  3.00000E-04  0.00000E+00  0.00000E+00  0.00000E+00  "1:Load Case 1" 
  
 DIRECT SUMMATION OF NODE REACTION FORCES 
   Case        FX           FY           FZ           MX           MY           MZ       Case Name 
      1   +0.00000E+00 +0.00000E+00 -1.00000E+04 +0.00000E+00 +0.00000E+00 +0.00000E+00  "1:Load Case 1" 
  
 TOTAL CPU TIME              : 0.719 Seconds 
  
 
*SUMMARY OF MESSAGES
*Number of Notes    : 0
*Number of Warnings : 1
*Number of Errors   : 0
 
*SOLUTION COMPLETED AT 14:11 ON 02/04/2026 
*SOLUTION TIME: 3 Seconds 
