import datetime
import time
from main import MyUser

def getAdjDays(currentUser):
    now = datetime.date.today()
    d = now - currentUser.dob
    age = d.days / 365.4
    if currentUser.gender is not None:
        g = currentUser.gender
        if g == "Female":
            if currentUser.ethnicity is not None:
                e = currentUser.ethnicity
                if e == "White":
                    adjDays = wrf(age)
                elif e == "Black":
                    adjDays = brf(age)
                elif e == "Hispanic":
                    adjDays = hrf(age)
                elif e == "Native American":
                    adjDays = nrf(age)
                elif e == "Alaskan Native":
                    adjDays = krf(age)
                elif e == "Asian / Pacific Islander":
                    adjDays = prf(age)
                else:
                    adjDays = arf(age)
            else:
                adjDays = arf(age)
        elif g == "Male":
            if currentUser.ethnicity is not None:
                e = currentUser.ethnicity
                if e == "White":
                    adjDays = wrm(age)
                elif e == "Black":
                    adjDays = brm(age)
                elif e == "Hispanic":
                    adjDays = hrm(age)
                elif e == "Native American":
                    adjDays = nrm(age)
                elif e == "Alaskan Native":
                    adjDays = krm(age)
                elif e == "Asian / Pacific Islander":
                    adjDays = prm(age)
                else:
                    adjDays = arm(age)
            else:
                adjDays = arm(age)
        else:
            adjDays = arb(age)
    elif currentUser.ethnicity is not None:
        e = currentUser.ethnicity
        if e == "White":
            adjDays = wrb(age)
        elif e == "Black":
            adjDays = brb(age)
        elif e == "Hispanic":
            adjDays = hrb(age)
        elif e == "Native American":
            adjDays = nrb(age)
        elif e == "Alaskan Native":
            adjDays = krb(age)
        elif e == "Asian / Pacific Islander":
            adjDays = prb(age)
        else:
            adjDays = arb(age)
    else:
        adjDays = arb(age)

    if currentUser.bmi is not None and currentUser.bmi > 0:
        adjDays = bmiAdj(currentUser, adjDays)

    if currentUser.smoker is not None:
        adjDays = smokerAdj(currentUser, age, adjDays)

    if currentUser.country is not None:
        adjDays = countryAdj(currentUser, adjDays)

    return adjDays

def arb(AGE):
    ARB = ((0.00004681401833 * (AGE**3)) - (0.003268056416 * (AGE**2)) - (0.8978485239 * AGE) + 77.76649053) * 365.4
    return ARB

def arm(AGE):
    ARM = ((0.00004547396603 * (AGE**3)) - (0.002847651569 * (AGE**2)) - (0.9029265622 * AGE) + 75.23283551) * 365.4
    return ARM

def arf(AGE):
    ARF = ((0.00004897170894 * (AGE**3)) - (0.003773463804 * (AGE**2)) - (0.89783089 * AGE) + 80.24954134) * 365.4
    return ARF

def wrb(AGE):
    WRB = ((0.0000002839685463 * (AGE**4)) - (0.000008279359997 * (AGE**3)) + (0.00005667420752 * (AGE**2)) - (0.9674504727 * AGE) + 78.4) * 365.4
    return WRB

def wrm(AGE):
    WRM = ((0.0000002369410772 * (AGE**4)) + (0.0000001467779463 * (AGE**3)) - (0.0001801593533 * (AGE**2)) - (0.9578137917 * AGE) + 75.88006851) * 365.4
    return WRM

def wrf(AGE):
    WRF = ((0.0000003354962129 * (AGE**4)) - (0.00001681814915 * (AGE**3)) + (0.0002487129711 * (AGE**2)) - (0.9773644486 * AGE) + 80.82919902) * 365.4
    return WRF

def brb(AGE):
    BRB = ((-0.0000001059067204 * (AGE**4)) + (0.00005860236081 * (AGE**3)) - (0.00279834693 * (AGE**2)) - (0.9088139398 * AGE) + 73.71075273) * 365.4
    return BRB

def brm(AGE):
    BRM = ((-0.0000001922523195 * (AGE**4)) + (0.00007322609054 * (AGE**3)) - (0.00317864491 * (AGE**2)) - (0.8967244066 * AGE) + 70.15014952) * 365.4
    return BRM

def brf(AGE):
    BRF = ((0.000000006980212669 * (AGE**4)) + (0.0000397124524 * (AGE**3)) - (0.002157467768 * (AGE**2)) - (0.9304407138 * AGE) + 77.05118182) * 365.4
    return BRF

def hrb(AGE):
    HRB = arb(AGE) * 1.025
    return HRB

def hrm(AGE):
    HRM = arm(AGE) * 1.025
    return HRM

def hrf(AGE):
    HRF = arf(AGE) * 1.025
    return HRF

def nrb(AGE):
    NRB = arb(AGE) * 1.05
    return NRB

def nrm(AGE):
    NRM = arm(AGE) * 1.05
    return NRM

def nrf(AGE):
    NRF = arf(AGE) * 1.05
    return NRF

def krb(AGE):
    KRB = arb(AGE) * 1.075
    return KRB

def krm(AGE):
    KRM = arm(AGE) * 1.075
    return KRM

def krf(AGE):
    KRF = arf(AGE) * 1.075
    return KRF

def prb(AGE):
    PRB = arb(AGE) * 1.1
    return PRB

def prm(AGE):
    PRM = arm(AGE) * 1.1
    return PRM

def prf(AGE):
    PRF = arf(AGE) * 1.1
    return PRF

def bmiAdj(currentUser, adjDays):
    bmi = currentUser.bmi
    if currentUser.gender == "Male":
        adjDays *= (100 - ((0.0003149239497 * (bmi**4)) - (0.04225364821 * (bmi**3)) + (2.116579451 * (bmi**2)) - (45.83513675 * bmi) + 374.8497 - 14.85)) / 100
    elif currentUser.gender == "Female":
        adjDays *= (100 - ((0.0001085143521 * (bmi**4)) - (0.01549495919 * (bmi**3)) + (0.8258794367 * (bmi**2)) - (18.83887369 * bmi) + 163.309072 - 8.68)) / 100
    else:
        adjDays *= 1

    return adjDays

def smokerAdj(currentUser, AGE, adjDays):
    if currentUser.smoker == True:
        adjDays *= ((0.000276199495*(AGE**3))-(0.04600087413*(AGE**2))+(1.871891997*AGE)+61.20675991)/100
    else:
        adjDays *= 1

    return adjDays

def countryAdj(currentUser, adjDays):
    country = dict()
    country = {'US' : 1,
                'AF' : 0.5953,
                'AL' : 0.9287,
                'DZ' : 0.904,
                'AS' : 1,
                'AD' : 1.083,
                'AO' : 0.4968,
                'AI' : 1,
                'AQ' : 1,
                'AG' : 0.9144,
                'AR' : 0.9741,
                'AM' : 0.8612,
                'AW' : 1,
                'AU' : 1.035,
                'AT' : 1.0078,
                'AZ' : 0.8158,
                'BS' : 0.9222,
                'BH' : 0.9468,
                'BD' : 0.7808,
                'BB' : 0.9468,
                'BY' : 0.882,
                'BE' : 1.0091,
                'BZ' : 0.9196,
                'BJ' : 0.6511,
                'BM' : 1,
                'BT' : 0.6796,
                'BO' : 0.8262,
                'BA' : 0.9274,
                'BW' : 0.5097,
                'BV' : 1,
                'BR' : 0.8158,
                'IO' : 1,
                'BN' : 0.9546,
                'BG' : 0.9196,
                'BF' : 0.6057,
                'BI' : 0.5992,
                'KH' : 0.7328,
                'CM' : 0.7108,
                'CA' : 1.0298,
                'CV' : 0.8936,
                'KY' : 1,
                'CF' : 0.5707,
                'TD' : 0.655,
                'CL' : 0.9818,
                'CN' : 0.9261,
                'CX' : 1,
                'CC' : 1,
                'CO' : 0.9118,
                'KM' : 0.7782,
                'CG' : 0.6148,
                'CD' : 0.6329,
                'CK' : 1,
                'CR' : 0.9831,
                'CI' : 0.5863,
                'HR' : 0.9559,
                'CU' : 0.9883,
                'CY' : 0.9948,
                'CZ' : 0.9663,
                'DK' : 0.9922,
                'DJ' : 0.6589,
                'DM' : 0.952,
                'DO' : 0.9494,
                'TP' : 1,
                'EC' : 0.9222,
                'EG' : 0.821,
                'SV' : 0.904,
                'GQ' : 0.6952,
                'ER' : 0.7237,
                'EE' : 0.9014,
                'ET' : 0.5863,
                'FK' : 1,
                'FO' : 1,
                'FJ' : 0.8807,
                'FI' : 1.0039,
                'FR' : 1.022,
                'FX' : 1,
                'GF' : 1,
                'PF' : 1,
                'TF' : 1,
                'GA' : 0.6498,
                'GM' : 0.69,
                'GE' : 0.8366,
                'DE' : 1.0039,
                'GH' : 0.7445,
                'GI' : 1,
                'GR' : 1.0169,
                'GL' : 1,
                'GD' : 0.8366,
                'GP' : 1,
                'GU' : 1,
                'GT' : 0.8586,
                'GN' : 0.5914,
                'GW' : 0.6355,
                'GY' : 0.8301,
                'HT' : 0.6381,
                'HM' : 1,
                'VA' : 1,
                'HN' : 0.9066,
                'HK' : 1,
                'HU' : 0.9261,
                'IS' : 1.0298,
                'IN' : 0.8106,
                'ID' : 0.882,
                'IR' : 0.904,
                'IQ' : 0.8625,
                'IE' : 0.9961,
                'IL' : 1.0195,
                'IT' : 1.0246,
                'JM' : 0.9754,
                'JP' : 1.0467,
                'JO' : 1.0039,
                'KZ' : 0.8197,
                'KE' : 0.6226,
                'KI' : 0.7756,
                'KP' : 0.917,
                'KR' : 0.965,
                'KW' : 0.9663,
                'KG' : 0.8223,
                'LA' : 0.6887,
                'LV' : 0.8872,
                'LB' : 0.9248,
                'LS' : 0.6589,
                'LR' : 0.6615,
                'LY' : 0.9792,
                'LI' : 1.022,
                'LT' : 0.8962,
                'LU' : 1,
                'MO' : 1,
                'MK' : 0.9572,
                'MG' : 0.7134,
                'MW' : 0.4877,
                'MY' : 0.9183,
                'MV' : 0.8067,
                'ML' : 0.6057,
                'MT' : 1.0104,
                'MH' : 0.8495,
                'MQ' : 1,
                'MR' : 0.6589,
                'MU' : 0.9209,
                'YT' : 1,
                'MX' : 0.9274,
                'FM' : 0.8898,
                'MD' : 0.8366,
                'MC' : 1.022,
                'MN' : 0.8729,
                'MS' : 1,
                'MA' : 0.8962,
                'MZ' : 0.4864,
                'MM' : 0.7121,
                'NA' : 0.5512,
                'NR' : 0.7886,
                'NP' : 0.7497,
                'NL' : 1.0156,
                'AN' : 1,
                'NC' : 1,
                'NZ' : 1.0091,
                'NI' : 0.8911,
                'NE' : 0.5357,
                'NG' : 0.6693,
                'NU' : 1,
                'NF' : 1,
                'MP' : 1,
                'NO' : 1.0208,
                'OM' : 0.9313,
                'PK' : 0.7925,
                'PW' : 0.8898,
                'PA' : 0.9792,
                'PG' : 0.8184,
                'PY' : 0.9559,
                'PE' : 0.9079,
                'PH' : 0.8755,
                'PN' : 1,
                'PL' : 0.9494,
                'PT' : 0.9831,
                'PR' : 1,
                'QA' : 0.939,
                'RE' : 1,
                'RO' : 0.9066,
                'RU' : 0.8716,
                'RW' : 0.5097,
                'KN' : 0.917,
                'LC' : 0.9377,
                'VC' : 1,
                'WS' : 0.8975,
                'SM' : 1.0519,
                'ST' : 0.847,
                'SA' : 0.8794,
                'SN' : 0.8067,
                'RS' : 0.939,
                'SC' : 0.9131,
                'SL' : 0.5875,
                'SG' : 1.0389,
                'SK' : 0.9559,
                'SI' : 0.9715,
                'SB' : 0.9248,
                'SO' : 0.5992,
                'ZA' : 0.6628,
                'GS' : 1,
                'ES' : 1.022,
                'LK' : 0.9313,
                'SH' : 1,
                'PM' : 1,
                'SD' : 0.7341,
                'SR' : 0.9261,
                'SJ' : 1,
                'SZ' : 0.524,
                'SE' : 1.0324,
                'CH' : 1.0324,
                'SY' : 0.8885,
                'TW' : 0.9909,
                'TJ' : 0.8314,
                'TZ' : 0.6783,
                'TH' : 0.8898,
                'TG' : 0.7095,
                'TK' : 1,
                'TO' : 0.8807,
                'TT' : 0.882,
                'TN' : 0.9559,
                'TR' : 0.9209,
                'TM' : 0.7899,
                'TC' : 1,
                'TV' : 0.8599,
                'UG' : 0.5564,
                'UA' : 0.856,
                'AE' : 0.9611,
                'GB' : 1.0078,
                'UM' : 1,
                'UY' : 0.9754,
                'UZ' : 0.8262,
                'VU' : 0.786,
                'VE' : 0.9481,
                'VN' : 0.8988,
                'VG' : 1,
                'VI' : 1,
                'WF' : 1,
                'EH' : 1,
                'YE' : 0.7756,
                'YU' : 1,
                'ZM' : 0.4825,
                'ZW' : 0.4903,
    }

    adj = country.get(currentUser.country, None)
    if adj is not None:
        adjDays *= adj
    else:
        adjDays *= 1

    return adjDays
