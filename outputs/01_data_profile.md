#

## DETAILED PROFILING OUTPUT

```
Detailed Statistics:
       mean radius  mean texture  mean perimeter    mean area  \
count   569.000000    569.000000      569.000000   569.000000   
mean     14.127292     19.289649       91.969033   654.889104   
std       3.524049      4.301036       24.298981   351.914129   
min       6.981000      9.710000       43.790000   143.500000   
25%      11.700000     16.170000       75.170000   420.300000   
50%      13.370000     18.840000       86.240000   551.100000   
75%      15.780000     21.800000      104.100000   782.700000   
max      28.110000     39.280000      188.500000  2501.000000   

       mean smoothness  mean compactness  mean concavity  mean concave points  \
count       569.000000        569.000000      569.000000           569.000000   
mean          0.096360          0.104341        0.088799             0.048919   
std           0.014064          0.052813        0.079720             0.038803   
min           0.052630          0.019380        0.000000             0.000000   
25%           0.086370          0.064920        0.029560             0.020310   
50%           0.095870          0.092630        0.061540             0.033500   
75%           0.105300          0.130400        0.130700             0.074000   
max           0.163400          0.345400        0.426800             0.201200   

       mean symmetry  mean fractal dimension  ...  worst texture  \
count     569.000000              569.000000  ...     569.000000   
mean        0.181162                0.062798  ...      25.677223   
std         0.027414                0.007060  ...       6.146258   
min         0.106000                0.049960  ...      12.020000   
25%         0.161900                0.057700  ...      21.080000   
50%         0.179200                0.061540  ...      25.410000   
75%         0.195700                0.066120  ...      29.720000   
max         0.304000                0.097440  ...      49.540000   

       worst perimeter   worst area  worst smoothness  worst compactness  \
count       569.000000   569.000000        569.000000         569.000000   
mean        107.261213   880.583128          0.132369           0.254265   
std          33.602542   569.356993          0.022832           0.157336   
min          50.410000   185.200000          0.071170           0.027290   
25%          84.110000   515.300000          0.116600           0.147200   
50%          97.660000   686.500000          0.131300           0.211900   
75%         125.400000  1084.000000          0.146000           0.339100   
max         251.200000  4254.000000          0.222600           1.058000   

       worst concavity  worst concave points  worst symmetry  \
count       569.000000            569.000000      569.000000   
mean          0.272188              0.114606        0.290076   
std           0.208624              0.065732        0.061867   
min           0.000000              0.000000        0.156500   
25%           0.114500              0.064930        0.250400   
50%           0.226700              0.099930        0.282200   
75%           0.382900              0.161400        0.317900   
max           1.252000              0.291000        0.663800   

       worst fractal dimension   diagnosis  
count               569.000000  569.000000  
mean                  0.083946    0.627417  
std                   0.018061    0.483918  
min                   0.055040    0.000000  
25%                   0.071460    0.000000  
50%                   0.080040    1.000000  
75%                   0.092080    1.000000  
max                   0.207500    1.000000  

[8 rows x 31 columns]

Correlation Matrix:
                         mean radius  mean texture  mean perimeter  mean area  \
mean radius                 1.000000      0.323782        0.997855   0.987357   
mean texture                0.323782      1.000000        0.329533   0.321086   
mean perimeter              0.997855      0.329533        1.000000   0.986507   
mean area                   0.987357      0.321086        0.986507   1.000000   
mean smoothness             0.170581     -0.023389        0.207278   0.177028   
mean compactness            0.506124      0.236702        0.556936   0.498502   
mean concavity              0.676764      0.302418        0.716136   0.685983   
mean concave points         0.822529      0.293464        0.850977   0.823269   
mean symmetry               0.147741      0.071401        0.183027   0.151293   
mean fractal dimension     -0.311631     -0.076437       -0.261477  -0.283110   
radius error                0.679090      0.275869        0.691765   0.732562   
texture error              -0.097317      0.386358       -0.086761  -0.066280   
perimeter error             0.674172      0.281673        0.693135   0.726628   
area error                  0.735864      0.259845        0.744983   0.800086   
smoothness error           -0.222600      0.006614       -0.202694  -0.166777   
compactness error           0.206000      0.191975        0.250744   0.212583   
concavity error             0.194204      0.143293        0.228082   0.207660   
concave points error        0.376169      0.163851        0.407217   0.372320   
symmetry error             -0.104321      0.009127       -0.081629  -0.072497   
fractal dimension error    -0.042641      0.054458       -0.005523  -0.019887   
worst radius                0.969539      0.352573        0.969476   0.962746   
worst texture               0.297008      0.912045        0.303038   0.287489   
worst perimeter             0.965137      0.358040        0.970387   0.959120   
worst area                  0.941082      0.343546        0.941550   0.959213   
worst smoothness            0.119616      0.077503        0.150549   0.123523   
worst compactness           0.413463      0.277830        0.455774   0.390410   
worst concavity             0.526911      0.301025        0.563879   0.512606   
worst concave points        0.744214      0.295316        0.771241   0.722017   
worst symmetry              0.163953      0.105008        0.189115   0.143570   
worst fractal dimension     0.007066      0.119205        0.051019   0.003738   
diagnosis                  -0.730029     -0.415185       -0.742636  -0.708984   

                         mean smoothness  mean compactness  mean concavity  \
mean radius                     0.170581          0.506124        0.676764   
mean texture                   -0.023389          0.236702        0.302418   
mean perimeter                  0.207278          0.556936        0.716136   
mean area                       0.177028          0.498502        0.685983   
mean smoothness                 1.000000          0.659123        0.521984   
mean compactness                0.659123          1.000000        0.883121   
mean concavity                  0.521984          0.883121        1.000000   
mean concave points             0.553695          0.831135        0.921391   
mean symmetry                   0.557775          0.602641        0.500667   
mean fractal dimension          0.584792          0.565369        0.336783   
radius error                    0.301467          0.497473        0.631925   
texture error                   0.068406          0.046205        0.076218   
perimeter error                 0.296092          0.548905        0.660391   
area error                      0.246552          0.455653        0.617427   
smoothness error                0.332375          0.135299        0.098564   
compactness error               0.318943          0.738722        0.670279   
concavity error                 0.248396          0.570517        0.691270   
concave points error            0.380676          0.642262        0.683260   
symmetry error                  0.200774          0.229977        0.178009   
fractal dimension error         0.283607          0.507318        0.449301   
worst radius                    0.213120          0.535315        0.688236   
worst texture                   0.036072          0.248133        0.299879   
worst perimeter                 0.238853          0.590210        0.729565   
worst area                      0.206718          0.509604        0.675987   
worst smoothness                0.805324          0.565541        0.448822   
worst compactness               0.472468          0.865809        0.754968   
worst concavity                 0.434926          0.816275        0.884103   
worst concave points            0.503053          0.815573        0.861323   
worst symmetry                  0.394309          0.510223        0.409464   
worst fractal dimension         0.499316          0.687382        0.514930   
diagnosis                      -0.358560         -0.596534       -0.696360   

                         mean concave points  mean symmetry  \
mean radius                         0.822529       0.147741   
mean texture                        0.293464       0.071401   
mean perimeter                      0.850977       0.183027   
mean area                           0.823269       0.151293   
mean smoothness                     0.553695       0.557775   
mean compactness                    0.831135       0.602641   
mean concavity                      0.921391       0.500667   
mean concave points                 1.000000       0.462497   
mean symmetry                       0.462497       1.000000   
mean fractal dimension              0.166917       0.479921   
radius error                        0.698050       0.303379   
texture error                       0.021480       0.128053   
perimeter error                     0.710650       0.313893   
area error                          0.690299       0.223970   
smoothness error                    0.027653       0.187321   
compactness error                   0.490424       0.421659   
concavity error                     0.439167       0.342627   
concave points error                0.615634       0.393298   
symmetry error                      0.095351       0.449137   
fractal dimension error             0.257584       0.331786   
worst radius                        0.830318       0.185728   
worst texture                       0.292752       0.090651   
worst perimeter                     0.855923       0.219169   
worst area                          0.809630       0.177193   
worst smoothness                    0.452753       0.426675   
worst compactness                   0.667454       0.473200   
worst concavity                     0.752399       0.433721   
worst concave points                0.910155       0.430297   
worst symmetry                      0.375744       0.699826   
worst fractal dimension             0.368661       0.438413   
diagnosis                          -0.776614      -0.330499   

                         mean fractal dimension  ...  worst texture  \
mean radius                           -0.311631  ...       0.297008   
mean texture                          -0.076437  ...       0.912045   
mean perimeter                        -0.261477  ...       0.303038   
mean area                             -0.283110  ...       0.287489   
mean smoothness                        0.584792  ...       0.036072   
mean compactness                       0.565369  ...       0.248133   
mean concavity                         0.336783  ...       0.299879   
mean concave points                    0.166917  ...       0.292752   
mean symmetry                          0.479921  ...       0.090651   
mean fractal dimension                 1.000000  ...      -0.051269   
radius error                           0.000111  ...       0.194799   
texture error                          0.164174  ...       0.409003   
perimeter error                        0.039830  ...       0.200371   
area error                            -0.090170  ...       0.196497   
smoothness error                       0.401964  ...      -0.074743   
compactness error                      0.559837  ...       0.143003   
concavity error                        0.446630  ...       0.100241   
concave points error                   0.341198  ...       0.086741   
symmetry error                         0.345007  ...      -0.077473   
fractal dimension error                0.688132  ...      -0.003195   
worst radius                          -0.253691  ...       0.359921   
worst texture                         -0.051269  ...       1.000000   
worst perimeter                       -0.205151  ...       0.365098   
worst area                            -0.231854  ...       0.345842   
worst smoothness                       0.504942  ...       0.225429   
worst compactness                      0.458798  ...       0.360832   
worst concavity                        0.346234  ...       0.368366   
worst concave points                   0.175325  ...       0.359755   
worst symmetry                         0.334019  ...       0.233027   
worst fractal dimension                0.767297  ...       0.219122   
diagnosis                              0.012838  ...      -0.456903   

                         worst perimeter  worst area  worst smoothness  \
mean radius                     0.965137    0.941082          0.119616   
mean texture                    0.358040    0.343546          0.077503   
mean perimeter                  0.970387    0.941550          0.150549   
mean area                       0.959120    0.959213          0.123523   
mean smoothness                 0.238853    0.206718          0.805324   
mean compactness                0.590210    0.509604          0.565541   
mean concavity                  0.729565    0.675987          0.448822   
mean concave points             0.855923    0.809630          0.452753   
mean symmetry                   0.219169    0.177193          0.426675   
mean fractal dimension         -0.205151   -0.231854          0.504942   
radius error                    0.719684    0.751548          0.141919   
texture error                  -0.102242   -0.083195         -0.073658   
perimeter error                 0.721031    0.730713          0.130054   
area error                      0.761213    0.811408          0.125389   
smoothness error               -0.217304   -0.182195          0.314457   
compactness error               0.260516    0.199371          0.227394   
concavity error                 0.226680    0.188353          0.168481   
concave points error            0.394999    0.342271          0.215351   
symmetry error                 -0.103753   -0.110343         -0.012662   
fractal dimension error        -0.001000   -0.022736          0.170568   
worst radius                    0.993708    0.984015          0.216574   
worst texture                   0.365098    0.345842          0.225429   
worst perimeter                 1.000000    0.977578          0.236775   
worst area                      0.977578    1.000000          0.209145   
worst smoothness                0.236775    0.209145          1.000000   
worst compactness               0.529408    0.438296          0.568187   
worst concavity                 0.618344    0.543331          0.518523   
worst concave points            0.816322    0.747419          0.547691   
worst symmetry                  0.269493    0.209146          0.493838   
worst fractal dimension         0.138957    0.079647          0.617624   
diagnosis                      -0.782914   -0.733825         -0.421465   

                         worst compactness  worst concavity  \
mean radius                       0.413463         0.526911   
mean texture                      0.277830         0.301025   
mean perimeter                    0.455774         0.563879   
mean area                         0.390410         0.512606   
mean smoothness                   0.472468         0.434926   
mean compactness                  0.865809         0.816275   
mean concavity                    0.754968         0.884103   
mean concave points               0.667454         0.752399   
mean symmetry                     0.473200         0.433721   
mean fractal dimension            0.458798         0.346234   
radius error                      0.287103         0.380585   
texture error                    -0.092439        -0.068956   
perimeter error                   0.341919         0.418899   
area error                        0.283257         0.385100   
smoothness error                 -0.055558        -0.058298   
compactness error                 0.678780         0.639147   
concavity error                   0.484858         0.662564   
concave points error              0.452888         0.549592   
symmetry error                    0.060255         0.037119   
fractal dimension error           0.390159         0.379975   
worst radius                      0.475820         0.573975   
worst texture                     0.360832         0.368366   
worst perimeter                   0.529408         0.618344   
worst area                        0.438296         0.543331   
worst smoothness                  0.568187         0.518523   
worst compactness                 1.000000         0.892261   
worst concavity                   0.892261         1.000000   
worst concave points              0.801080         0.855434   
worst symmetry                    0.614441         0.532520   
worst fractal dimension           0.810455         0.686511   
diagnosis                        -0.590998        -0.659610   

                         worst concave points  worst symmetry  \
mean radius                          0.744214        0.163953   
mean texture                         0.295316        0.105008   
mean perimeter                       0.771241        0.189115   
mean area                            0.722017        0.143570   
mean smoothness                      0.503053        0.394309   
mean compactness                     0.815573        0.510223   
mean concavity                       0.861323        0.409464   
mean concave points                  0.910155        0.375744   
mean symmetry                        0.430297        0.699826   
mean fractal dimension               0.175325        0.334019   
radius error                         0.531062        0.094543   
texture error                       -0.119638       -0.128215   
perimeter error                      0.554897        0.109930   
area error                           0.538166        0.074126   
smoothness error                    -0.102007       -0.107342   
compactness error                    0.483208        0.277878   
concavity error                      0.440472        0.197788   
concave points error                 0.602450        0.143116   
symmetry error                      -0.030413        0.389402   
fractal dimension error              0.215204        0.111094   
worst radius                         0.787424        0.243529   
worst texture                        0.359755        0.233027   
worst perimeter                      0.816322        0.269493   
worst area                           0.747419        0.209146   
worst smoothness                     0.547691        0.493838   
worst compactness                    0.801080        0.614441   
worst concavity                      0.855434        0.532520   
worst concave points                 1.000000        0.502528   
worst symmetry                       0.502528        1.000000   
worst fractal dimension              0.511114        0.537848   
diagnosis                           -0.793566       -0.416294   

                         worst fractal dimension  diagnosis  
mean radius                             0.007066  -0.730029  
mean texture                            0.119205  -0.415185  
mean perimeter                          0.051019  -0.742636  
mean area                               0.003738  -0.708984  
mean smoothness                         0.499316  -0.358560  
mean compactness                        0.687382  -0.596534  
mean concavity                          0.514930  -0.696360  
mean concave points                     0.368661  -0.776614  
mean symmetry                           0.438413  -0.330499  
mean fractal dimension                  0.767297   0.012838  
radius error                            0.049559  -0.567134  
texture error                          -0.045655   0.008303  
perimeter error                         0.085433  -0.556141  
area error                              0.017539  -0.548236  
smoothness error                        0.101480   0.067016  
compactness error                       0.590973  -0.292999  
concavity error                         0.439329  -0.253730  
concave points error                    0.310655  -0.408042  
symmetry error                          0.078079   0.006522  
fractal dimension error                 0.591328  -0.077972  
worst radius                            0.093492  -0.776454  
worst texture                           0.219122  -0.456903  
worst perimeter                         0.138957  -0.782914  
worst area                              0.079647  -0.733825  
worst smoothness                        0.617624  -0.421465  
worst compactness                       0.810455  -0.590998  
worst concavity                         0.686511  -0.659610  
worst concave points                    0.511114  -0.793566  
worst symmetry                          0.537848  -0.416294  
worst fractal dimension                 1.000000  -0.323872  
diagnosis                              -0.323872   1.000000  

[31 rows x 31 columns]

Value Counts for Categorical Columns:
diagnosis
1    357
0    212
Name: count, dtype: int64

Missing Value Percentages:
mean radius                0.0
mean texture               0.0
mean perimeter             0.0
mean area                  0.0
mean smoothness            0.0
mean compactness           0.0
mean concavity             0.0
mean concave points        0.0
mean symmetry              0.0
mean fractal dimension     0.0
radius error               0.0
texture error              0.0
perimeter error            0.0
area error                 0.0
smoothness error           0.0
compactness error          0.0
concavity error            0.0
concave points error       0.0
symmetry error             0.0
fractal dimension error    0.0
worst radius               0.0
worst texture              0.0
worst perimeter            0.0
worst area                 0.0
worst smoothness           0.0
worst compactness          0.0
worst concavity            0.0
worst concave points       0.0
worst symmetry             0.0
worst fractal dimension    0.0
diagnosis                  0.0
dtype: float64

Target Variable Distribution:
diagnosis
1    0.627417
0    0.372583
Name: proportion, dtype: float64

Data Type Information:
mean radius                float64
mean texture               float64
mean perimeter             float64
mean area                  float64
mean smoothness            float64
mean compactness           float64
mean concavity             float64
mean concave points        float64
mean symmetry              float64
mean fractal dimension     float64
radius error               float64
texture error              float64
perimeter error            float64
area error                 float64
smoothness error           float64
compactness error          float64
concavity error            float64
concave points error       float64
symmetry error             float64
fractal dimension error    float64
worst radius               float64
worst texture              float64
worst perimeter            float64
worst area                 float64
worst smoothness           float64
worst compactness          float64
worst concavity            float64
worst concave points       float64
worst symmetry             float64
worst fractal dimension    float64
diagnosis                    int64
dtype: object
```