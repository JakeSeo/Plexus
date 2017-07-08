production_attribute_names = ['no_hh', 'no_mem', 'no_mem_educwork',
                   'lu_ind_commercial', 'lu_ind_parks', 'lu_ind_industrial',
                   'lu_ind_agriculture','lu_ind_residential', 'lu_ind_utilities']
production_attribute_names2 = ['no_hh', 'avg_income','no_mem', 'no_mem_educ', 'no_mem_work',
                   'lu_ind_commercial', 'lu_ind_parks', 'lu_ind_industrial',
                   'lu_ind_agriculture','lu_ind_residential', 'lu_ind_utilities','lu_ind_others']
production_attribute_intercept = 0
production_attribute_coeffiients = [3.29147761e+00,   2.08982787e-20,   5.28792145e-22,   5.61467426e-19,
   6.00000000e+02,   4.40542048e-20,   1.94194107e-14,   1.55278782e+02,
   4.20451846e-21,   1.00000000e-01]


attraction_attribute_names = ['no_amty_sustenance', 'no_amty_education', 'no_amty_transport', 'no_amty_healthcare',
                   'no_amty_finance', 'no_amty_commerce', 'no_amty_entertainment', 'no_amty_other',
                   'lu_ind_commercial', 'lu_ind_parks', 'lu_ind_industrial', 'lu_ind_agriculture',
                   'lu_ind_residential', 'lu_ind_utilities','lu_ind_others']
attraction_attribute_intercept = 4805.98183877
attraction_attribute_coeffiients = [2.54890477e-15,   1.10000000e+03,   1.30374385e+02,   1.75348756e+02,
   7.35037140e-15,   1.36839648e-19,   2.27627021e-14,   1.10000000e+03,
   3.99399310e+02,   1.10000000e+03,   1.10000000e+03,   3.42146846e+02,
   1.55961256e+02,   3.70819319e-17,   1.00000000e-01]
#

#Prod Intercept:-1334.37618541 Coef:[  65.38103342   11.84731132  -39.93400213    8.23285102  -25.241787
  # -1.2510184     2.20551241   31.82834803    3.07411895 -483.96528568
   # 0.        ]
#Attr Intercept:4805.98183877 Coef:[  -49.6028897     -4.83505864  -154.53369632   312.99534481    19.79017006
  #-980.65529731  1164.01053445    58.86796291    13.15743504    81.67469428
 #  -14.09065401    10.80746015     6.22225556 -3549.39096573     0.        ]