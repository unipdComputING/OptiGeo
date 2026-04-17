*SOLUTION COMMENCED AT 23:38 ON 08/04/2026 
  
 Straus7 [R3.1.6][Solver Build R3.1.6] (64-Bit) [STUDENT VERSION - EDUCATIONAL USE ONLY] 
  
 LICENCED TO                 : Antonio Valeriano 
  
 ANALYSIS TYPE               : LINEAR STATIC 
  
 COMPUTER NAME               : MUFFIN 
 USER LOGON NAME             : frank 
 CPU                         : AMD Ryzen 7 5700U with Radeon Graphics  
 USABLE PHYSICAL MEMORY      : 15.3 GB 
 USABLE VIRTUAL MEMORY       : 22.1 GB 
  
 MODEL FILE                  : "C:\Users\frank\OneDrive\Desktop\Antonio\Università\2_MAGISTRALE\1 ANNO\femDEV\Optigeo2026\TestFE\Exa8\Taglio Semplice.st7" 
 RESULT FILE                 : "C:\Users\frank\OneDrive\Desktop\Antonio\Università\2_MAGISTRALE\1 ANNO\femDEV\Optigeo2026\TestFE\Exa8\Taglio Semplice.LSA" 
 SCRATCH PATH                : "C:\Users\frank\Straus7 R31\Tmp\" 
  
 TOTALS 
 Nodes                       : 8 
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
  
 NUMBER OF EQUATIONS         : 4 
 MATRIX FILL-IN              : 0.0% 
 [K] MATRIX SIZE             : < 1 KB 
 OPTIMUM RAM NEEDED          : 128.0 KB 
 FREE SCRATCH SPACE          : 206.3 GB 
  
*WARNING[237]:Default freedom conditions might be over-constrained - one or more elements might require additional freedoms. 
  
 SUMMATION OF APPLIED LOADS  
          Case        FX           FY           FZ           MX           MY           MZ        Case Name 
 Nodes       1   -4.00000E+03 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
 Bricks      1   +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
 Total       1   -4.00000E+03 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
 Vector      1   -4.00000E+03 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00 +0.00000E+00   "1:Load Case 1" 
  
 SUMMATION OF MOMENTS OF APPLIED LOADS ABOUT THE ORIGIN [Vector]  
          Case        MXo          MYo          MZo       Case Name 
             1   +0.00000E+00 -4.00000E+06 +2.00000E+06   "1:Load Case 1" 
  
 Reducing 4 equations using 128.0 KB RAM for [K] of < 1 KB... 
  
 MAXIMUM PIVOT               : 4.000000E+07 (Node 5 DX) 
 MINIMUM PIVOT               : 3.137931E+07 (Node 8 DX) 
  
 Results for 1 load case... 
  
 MAXIMUM NODE DISPLACEMENT MAGNITUDES 
   Case        DX           DY           DZ           RX           RY           RZ       Case Name 
      1    5.00000E-05  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  "1:Load Case 1" 
  
 DIRECT SUMMATION OF NODE REACTION FORCES 
   Case        FX           FY           FZ           MX           MY           MZ       Case Name 
      1   +4.00000E+03 +2.48690E-14 -2.27374E-13 +0.00000E+00 +0.00000E+00 +0.00000E+00  "1:Load Case 1" 
  
 TOTAL CPU TIME              : 0.344 Seconds 
  
 
*SUMMARY OF MESSAGES
*Number of Notes    : 0
*Number of Warnings : 1
*Number of Errors   : 0
 
*SOLUTION COMPLETED AT 23:38 ON 08/04/2026 
*SOLUTION TIME: 3 Seconds 
