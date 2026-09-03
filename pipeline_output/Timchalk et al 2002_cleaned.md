A Physiologically Based Pharmacokinetic and Pharmacodynamic
(PBPK/PD) Model for the Organophosphate Insecticide
Chlorpyrifos in Rats and Humans
C. Timchalk,*
,1 R. J. Nolan,† A. L. Mendrala,‡ D. A. Dittenber,‡ K. A. Brzak,‡ and J. L. Mattsson†
*Battelle Paciﬁc Northwest Division, Chemical Dosimetry, PO Box 999, Richland, Washington 99352; †Dow AgroSciences,
9330 Zionsville, Indianapolis, Indiana 46268; and ‡The Dow Chemical Co., Midland, Michigan 48674
Received August 16, 2001; accepted November 28, 2001
A PBPK/PD model was developed for the organophosphate insec-
ticide chlorpyrifos (CPF) (O,O-diethyl-O-[3,5,6-trichloro-2-pyridyl]-
phosphorothioate), and the major metabolites CPF-oxon and 3,5,6-
trichloro-2-pyridinol (TCP) in rats and humans. This model
integrates target tissue dosimetry and dynamic response (i.e., esterase
inhibition) describing uptake, metabolism, and disposition of CPF,
CPF-oxon, and TCP and the associated cholinesterase (ChE) inhibi-
tion kinetics in blood and tissues following acute and chronic oral and
dermal exposure. To facilitate model development, single oral-dose
pharmacokinetic studies were conducted in rats (0.5–100 mg/kg) and
humans (0.5–2 mg/kg), and the kinetics of CPF, CPF-oxon, and TCP
were determined, as well as the extent of blood (plasma/RBC) and
brain (rats only) ChE inhibition. In blood, the concentration of ana-
lytes followed the order TCP >> CPF >> CPF-oxon; in humans
CPF-oxon was not quantiﬁable. Simulations were compared against
experimental data and previously published studies in rats and hu-
mans. The model was utilized to quantitatively compare dosimetry
and dynamic response between rats and humans over a range of CPF
doses. The time course of CPF and TCP in both species was linear
over the dose range evaluated, and the model reasonably simulated
the dose-dependent inhibition of plasma ChE, RBC acetylcholinest-
erase (AChE), and brain (rat only) AChE. Model simulations suggest
that rats exhibit greater metabolism of CPF to CPF-oxon than hu-
mans do, and that the depletion of nontarget B-esterase is associated
with a nonlinear, dose-dependent increase in CPF-oxon blood and
brain concentration. This CPF PBPK/PD model quantitatively esti-
mates target tissue dosimetry and AChE inhibition and is a strong
framework for further organophosphate (OP) model development
and for reﬁning a biologically based risk assessment for exposure to
CPF under a variety of scenarios.
Key Words: physiologically based pharmacokinetics; organo-
phosphate insecticide; chlorpyrifos; esterase inhibition.
Chlorpyrifos (O,O-diethyl-O-[3,5,6-trichloro-2-pyridyl]
phosphorothioate, CAS Registry No. 2921–88–2) is the active
ingredient in DURSBANt and LORSBANt insecticides.
Thionophosphorus organophosphates (OP) are a major sub-
group of broad spectrum OP insecticides that see widespread
commercial application, and their primary toxicological effect
is associated with the inhibition of acetylcholinesterase (AChE,
EC 3.1.1.7) in both central and peripheral nerve tissues (Mur-
phy, 1986; Sultatos, 1994). Phosphorothionates like chlorpyr-
ifos (CPF) do not directly inhibit AChE, but must ﬁrst be
metabolized to the corresponding oxygen analog (CPF-oxon).
The activation of CPF to CPF-oxon is mediated by cytochrome
P450 mixed-function oxidases (CYP450), primarily within the
liver. However, extrahepatic metabolism has been reported in
other tissues, including brain (Chambers and Chambers, 1989;
Guengerich, 1977). In addition, oxidative dearylation of CPF
to 3,5,6-trichloro-2-pyridinol (TCP) and diethylthiophosphate
represents a competing detoxiﬁcation pathway that is likewise
mediated by hepatic CYP450 (Ma and Chambers, 1994). In-
testinal CYP450 metabolism of drugs can be substantial (Hall
et al., 1999; Obach et al., 2001; Paine et al., 1999; Schmiedlin-
Ren, et al., 1993; Watkins, 1992; Zhang et al., 1999), and also
are likely to be important contributors to CPF metabolism.
Intestinal cells also contain multidrug resistance proteins (p-
glycoproteins) that react to CPF-oxon, and would likely be an
additional barrier to oxon absorption (Lanning et al., 1996).
Detoxiﬁcation reactions are believed to share a common
phosphooxythiran intermediate and represent critical biotrans-
formation steps required for toxicity (Neal, 1980). Differences
in the ratio of activation to detoxiﬁcation are believed to be
associated with sensitivity to OPs (Ma and Chambers, 1994).
Hepatic and extrahepatic A-esterase (A-EST, EC 3.1.1.1.2) can
effectively metabolize CPF-oxon to TCP (nontoxic metabolite)
and diethylphosphate without inactivating the enzyme (Sulta-
tos and Murphy, 1983). B-Esterases (B-EST) such as carboxy-
lesterase (CaE, EC 3.1.1.1), and butyrylcholinesterase (BuChE,
EC 3.1.1.8) can likewise detoxify CPF-oxon; however, these
B-ESTs become irreversibly bound (1:1 ratio) to the CPF-oxon
and thereby become inactivated (Chanda et al., 1977; Clement,
1984). Studies in both humans and rodents indicate that TCP
represents the primary metabolite of CPF, although glucuro-
Presented in part at the 37th annual meeting of the Society of Toxicology,
March, 1998, Seattle, Washington.
1 To whom correspondence should be addressed. Fax: (509) 376-9064.
E-mail: charles.timchalk@pnl.gov.
TOXICOLOGICAL SCIENCES 66, 34–53 (2002)
Copyright © 2002 by the Society of Toxicology

---CHUNK_BREAK---

E-mail: charles.timchalk@pnl.gov. TOXICOLOGICAL SCIENCES 66, 34–53 (2002) Copyright © 2002 by the Society of Toxicology nide and sulfate conjugates of TCP have likewise been ob-
served (Bakke et al., 1976; Nolan et al., 1984). Based on the extensive understanding of the biochemical
interactions between OPs and AChE, the relationship between
OP activation and detoxiﬁcation is of critical importance in
determining the toxicological response to OP insecticides (Ma
and Chamber, 1984). In this regard, Gearhart et al. (1990)
suggested that physiologically based pharmacokinetic and
pharmacodynamic (PBPK/PD) models capable of predicting
the relationship between OP exposure and AChE inhibition are
useful for evaluating the risk associated with a given OP
exposure. Although a limited number of PBPK/PD models for
OP insecticides and nerve agents have been published in the
literature (Abbas and Hayton, 1997; Gearhart et al., 1990;
Maxwell et al, 1988; Sultatos, 1990), there are currently no
models for the phosphorothionate insecticide CPF. The primary objective of the research reported herein was to
develop and validate a PBPK/PD model for CPF in rats and
humans. This model quantitatively integrates target tissue do-
simetry and dynamic response describing the pharmacokinetics
of CPF, CPF-oxon, and TCP, as well as the associated cho-
linesterase (ChE) inhibition kinetics in blood components
(plasma and red blood cell (RBC)) and selected tissues, includ-
ing the brain. To develop and validate the model, pharmaco-
kinetic/pharmacodynamic studies were conducted in both rats
and humans to quantitate dosimetry and dynamic response over
a range of CPF doses. In addition, the model was further
evaluated against available dosimetry and dynamic response
data in the published literature. MATERIALS AND METHODS
Chemicals. Chlorpyrifos was obtained from Dow AgroSciences (India-
napolis, IN) and had a chemical purity of 99.8%. 13C2-15N-Chlorpyrifos,
13C2-15N-chlorpyrifos-oxon, and 13C2-trichloropyridinol were utilized as inter-
nal standards for the negative-ion chemical ionization, gas chromatography–
mass spectrometry (NCI/GC/MS) for CPF, CPF-oxon, and TCP, respectively. Animals. Male Fischer 344 (F344) rats (Charles River Laboratories Inc.,
Raleigh, NC) were utilized for the pharmacokinetic/pharmacodynamic studies
(time points, 10 min–12 h postdosing) and were 10–11 weeks of age at the
time of dosing. Female F344 rats were purchased from the same supplier and
were also utilized to assess the pharmacodynamic response (time point, 24 h
postdosing) and were ;7 weeks of age at the start of the study. Animals were
housed one per cage (wire mesh or plastic), and maintained on a 12-h
photocycle, at controlled temperature (22–24°C), and relative humidity (44–
52%) and allowed access to municipal tap water and Purina certiﬁed rodent
chow ad libitum, except where otherwise noted. Model structure. A diagram of the PBPK/PD model structure developed
for CFP and CPF-oxon is illustrated in Figure 1 and is based on the model for
diisopropylﬂurophosphate (DFP) in rats (Gearhart et al., 1990). The current
PBPK/PD model was developed to describe the time course of absorption,
distribution, metabolism, and excretion of CPF, CPF-oxon, and TCP, and the
inhibition of target esterases by CPF-oxon in the rat and human. The model
assumes that the pharmacokinetic and pharmacodynamic response in rats and
humans is independent of gender, which is consistent with the observed
response in human males and females reported in this study. The absorption of
CPF following oral administration in corn oil vehicle required the use of a
two-compartment uptake model to simulate absorption, according to Staats et
al. (1991). This two-compartment model incorporated 1st-order rate equations
to describe systemic uptake and transfer between compartments. In addition,
absorption of CPF from the diet was incorporated into the model to allow for
the simulation of chronic dietary administration. In the chronic dietary studies
with CPF, the doses (mg/kg/day) determined were based upon the measured
rate of food consumption per day. To model the data, the absorbed dose was
expressed as a constant zero-order rate (mg/h) over a 12-h interval. This
assumption was reasonable since, in rats, the majority of the daily food intake
occurs during the lights-off cycle (;12 h) (Jochemsen et al., 1993). Equations
to describe the dermal uptake of CPF into the skin compartment of humans
were adapted from Poet et al. (2000). In this model, physiological and
metabolic parameters (i.e., tissue volume, blood ﬂow, and metabolic capacity)
were scaled as a function of body weight, according to the methods of Ramsey
and Andersen (1984). The CYP450-mediated activation and detoxiﬁcation of
CPF to CPF-oxon and TCP, respectively, was limited to the liver compartment. The model was linked to the CPF-oxon model that contained equations to
describe the A-EST hydrolysis of CPF-oxon to TCP in both the liver and blood
compartments. The CYP450 activation/detoxiﬁcation and A-EST detoxiﬁca-
tion of CPF-oxon were all described as Michaelis-Menten processes. Interac-
tions of the oxon with B-EST (AChE, BuChE, and CaE) were modeled as
2nd-order processes occurring in the liver, blood (plasma and RBC), brain, and
diaphragm. The B-EST enzyme levels (mmol) in blood, brain, liver, and
diaphragm were calculated based on the enzyme turnover rates and enzyme
activities reported by Maxwell et. al. (1987), and these were based on a balance
between basal degradation and enzyme resynthesis. Following exposure to
CPF-oxon, the amount of available B-EST was determined by ﬁnding a
balance between the bimolecular rate of inhibition and the rate of B-EST
regeneration (reactivation and resynthesis). In this model, TCP was formed by
the direct CYP450 metabolic conversion of CPF and through A-EST-mediated
hydrolysis of CPF-oxon and B-EST binding of CPF-oxon, respectively. The
blood kinetics and urinary elimination of TCP were described with a simple
one-compartment model utilizing a 1st-order rate of urinary elimination. Model parameters. To develop this model, several types of data were
required, including physiological constants, partition coefﬁcients, and bio-
chemical constants describing the metabolism of CPF, CPF-oxon, and the
inhibition of B-EST by CPF-oxon. These data were obtained from the litera-
ture, from experimentation, or by optimization of model output utilizing the
computer simulation. The PBPK/PD model code for simultaneous solution of
both algebraic and differential equations was developed in SIMUSOLVt, a
computer program containing a numerical integration, optimization, and
graphical routine, and is based on the Fortran-based software ACSL. The
values, assumptions, and references used for these parameters are listed in
Tables 1 and 2. Physiological constants and partition coefﬁcients. Organ volumes, car-
diac output, and tissue blood ﬂows were adapted from the DFP model devel-
oped by Gearheart et al. (1990) or obtained from the literature (Brown et al.,
1997). The partitioning coefﬁcients for CPF and CPF-oxon were estimated,
based on their octanol:water partitioning coefﬁcients and tissue lipid content
based on an algorithm developed by Poulin and Krishnan (1995). Biochemical constants. The metabolism of CPF to TCP and CPF-oxon is
mediated by CYP450 and is described using Michaelis-Menten kinetics. A
range of Km and Vmax parameters has been determined in vitro, utilizing tissue
obtained from both mice and rats (Ma and Chambers, 1994, 1995; Mortensen
et al., 1996; Pond et al., 1995; Sultatos and Murphy, 1983; Sultatos et al.,
1984). The selection of a reasonable set of model parameters was determined
by evaluating the overall goodness of ﬁt of the model against the experimental
data over the range of reported rate constants for enzyme afﬁnity and activities. Sultatos et al. (1984) previously reported that CPF was extensively bound
(;97%) to plasma proteins over a broad range of concentrations.

---CHUNK_BREAK---

that CPF was extensively bound (;97%) to plasma proteins over a broad range of concentrations. It was also
assumed that CPF-oxon would exhibit an even higher plasma protein binding
based upon oxon reactivity, although the extent of CPF-oxon plasma protein
binding has not yet been experimentally determined.

In the current model
structure, the total amount of absorbed CPF is directly added to the liver
compartment.

However, once in the systemic circulation, only nonbound (i.e.,

free) parent chemical or metabolite was capable of entering the tissue com-
partments.
B-esterase (B-EST) inhibition.
The model structure for the inhibition of
B-EST (AChE, BuChE, and CaE) by CPF-oxon in plasma, RBC, diaphragm,
and liver were likewise based on the model structure developed by Gearhart et
al. (1990). However, when available, CPF-speciﬁc model parameters for
bimolecular inhibition (Ki), reactivation (Kr), and aging (Ka) were incorpo-
rated into the model (Amitai et al., 1998; Carr and Chambers, 1996). Reacti-
vation and aging rates were not available for CPF-oxon inhibition of BuChE or
CaE so these parameters were set at the rates for CPF-oxon interaction with
AChE. The amount of enzyme (mmol), zero-order synthesis rate (mmol/h), and
1st-order degradation rate (h–1) of AChE, BuChE, and CaE for each of the
tissue compartments was calculated as previously described (Gearhart et al.
1990; Maxwell et al. 1987). The CaE enzyme degradation rate (Kd) and Ki
constants were estimated for each tissue by ﬁtting the model to data obtained
by Chanda et al. (1997). The Ki parameters for AChE and BuChE blood and
tissue activity were estimated by ﬁtting the experimental data from Figure 2.
The esterase recovery rates in the various tissue compartments were obtained
from a previous study (Gearhart et al., 1990) or by ﬁtting the oral dose plasma
BuChE data from Nolan et al. (1984).
In light of the importance of RBC AChE inhibition as a biomarker for OP
insecticide exposure, RBC AChE inhibition was incorporated into the
PBPK/PD model structure. The total amount of available RBC AChE (mmol)
in the rat was calculated based on the experimentally determined total RBC
FIG. 1.
Physiologically based pharmacokinetic and pharmacodynamic model used to describe the disposition of chlorpyrifos (CPF), CPF-oxon, and
trichloropyridinol (TCP), and B-esterase (B-EST) inhibition in rats and humans following oral (gavage, dietary) and dermal exposure to CPF. The shaded tissue
compartments indicate organs in which B-EST (AChE, BuChE and CaE) enzyme activity is described. Model parameter deﬁnitions: QC, cardiac output (l/h);
Qi, blood ﬂow to “i” tissue (l/h); Ca, arterial blood concentration of CPF (mmol/l); Cao, arterial blood concentration of CPF-oxon (mmol/l); Cv, pooled venous
blood concentration of CPF (mmol/l); Cvo, pooled venous blood concentration of CPF-oxon (mmol/l); Cvi, venous blood concentration of CPF draining “i” tissue
(mmol/l); Cvio, venous blood concentration of CPF-oxon draining “i” tissue (mmol/l); SA, surface area of skin exposed (cm2); KP, skin permeability coefﬁcient
(cm/h); Kzero, zero (mmol/h) rate of absorption of CPF from diet; Fa fractional absorption (%) gavage dose; KaS and KaI, 1st-order rate constant for absorption
of CPF from compartments 1 and 2 (per h); KsI, 1st-order rate constant for transfer of CPF from compartments 1 and 2 (per h); Ke, 1st-order rate constant for
elimination of TCP from compartment 3; Km1–4, Michaelis constant for saturable process (mmol/l); Vmax(1–4), maximum velocity for saturable process (mmol/h).

AChE enzyme activity in control animals. The Ki rate constant for RBC
inhibition was initially obtained from the literature (Amitai et al., 1998), and
the recovery of RBC AChE enzyme was based on the rate of RBC replenish-
ment, assuming a RBC lifespan of 50 and 122 days in the rat and human,
respectively (Schalm, 1961). Initial RBC AChE inhibition simulations in the
rat had a slower enzyme recovery, when compared against the results from a
previously published study (Nostrandt et al., 1997). Since RBC AChE resyn-
thesis was assumed to be primarily the result of new RBC formation, a slightly
faster reactivation rate (see Table 2) was required to account for the recovery
of RBC AChE activity observed 24 h postdosing.
Pharmacokinetic/Pharmacodynamic Studies
To develop and validate the CPF PBPK/PD model, pharmacokinetic/phar-
macodynamic studies were conducted in both rats and humans.
Rat.
The time course of CPF and CPF-oxon in the blood and the activity
of ChE in the plasma, and AChE in brains of male (F344) rats were determined
following oral administration of 100, 50, 10, 5, 1, and 0.5 mg CPF/kg of body
weight. An additional group of female rats were administered the same doses
of CPF and plasma; RBC, and selected tissue ChE activity was determined at
24 h postdosing. The dose solution was prepared in a corn oil vehicle and
administered by gavage, and all animals were fasted for approximately 16 h
prior to administration of CPF. Four animals per time point were humanely
anesthetized, sacriﬁced, and tissues were collected at 10 and 20 min, and 1, 3,
6, 12, and 24 h postdosing for CPF, CPF-oxon, or ChE analysis. The blood was
collected, via cardiac puncture, into heparinized syringes containing an acidic
salt solution (2.5 N acetic acid/saturated sodium chloride), which effectively
halted the enzymatic hydrolysis of CPF-oxon. These specimens were then
analyzed for the presence of CPF and CPF-oxon by NCI-GC-MS as described
by Brzak et al. (1998). The limit of quantitation (LOQ) for both CPF and
CPF-oxon was determined to be 3 nmol/l of blood. An additional blood sample
was collected at each time point, and centrifuged to separate the plasma and
RBC (24 h postdosing only) for analysis of plasma ChE and RBC AChE
activity. In addition, brains were removed, rapidly frozen by submersion in
liquid nitrogen, and both the plasma and brains were then stored at –80°C until
assayed for esterase activity. Brain and RBC AChE, and plasma ChE activity
assays were performed with Boehringer Mannheim (Indianapolis, IN) reagents
on a Hitachi 914 clinical chemistry analyzer utilizing acetylthiocholine (AcTh)
as an enzyme substrate, as previously described (Ellman et al., 1961).
Human volunteer pharmacokinetic study.
A double-blind, placebo-con-
trolled clinical pharmacokinetic study was conducted at MDS Harris Labora-
tory (Lincoln, NE), in accordance with all applicable U.S. guidelines as
speciﬁed in Title 21 of the Code of Federal Regulations (parts 50, 56 and 321)
and the International Guidelines for Human Testing as promulgated in the
Declaration of Helsinki (1964; amended 1996). The overall objective of this
study was to provide needed data to better deﬁne the pharmacokinetics of CPF
in humans. In this study, groups of 6 male and 6 female volunteers received a
single oral dose of 0, 0.5, 1, or 2 mg CPF/kg of body weight in capsule form.
The volunteers were conﬁned to the testing facility for the ﬁrst 24-h posttreat-
ment period, and their health status was closely monitored during this time,
providing a mechanism to conﬁrm the presence or absence of cholinergic or
other treatment-related effects. After the initial 24-h interval, the volunteers
were allowed to go home but continued to return to the testing facility for the
collection of additional blood specimens. Blood was collected at each interval
by venipuncture and the targeted collection intervals were 2, 4, 8, 12, 24, 36,
TABLE 1
Parameters used in the Physiologically Based Pharmacokinetic
Model for CPF and CPF-oxon to Describe Dosimetry and Metab-
olism
Parameter
Rat
Human
Estimation methoda
Percentage of body weight
Blood

Brain
1.2

Diaphragm
0.03
0.03
Fat

Liver

Rapidly perfused

Slowly perfused

Flows (l/h)
Cardiac output
5.4
347.9
% cardiac output
Brain

11.4
Diaphragm
0.6
0.6
Fat

5.2
Liver

Rapidly perfused
42.6

Slowly perfused

Skin
5.8
5.8
Partition coefﬁcients for CPF
Brain/blood

Diaphragm/blood

Fat/blood

Liver/blood

Rapidly perfused/blood

Slowly perfused/blood

Skin/blood

Partition coefﬁcients for CPF-oxon
Brain/blood

---CHUNK_BREAK---

CPF Brain/blood Diaphragm/blood Fat/blood Liver/blood Rapidly perfused/blood Slowly perfused/blood Skin/blood Partition coefﬁcients for CPF-oxon Brain/blood Diaphragm/blood
4.9
4.9
Fat/blood

Liver/blood

Rapidly perfused blood
8.1
8.1
Slowly perfused blood
4.9
4.9
Metabolic constants
CYP450 CPF-to- oxon (liver)
Km1 (mmol/l)
2.86
2.86
VmaxC1 (mmol/h/kg)

CYP450 CPF-to-TCP
Km2 (mmol/l)

VmaxC2 (mmol/h/kg)

A-EST oxon-to-TCP (liver)
Km3 (mmole/l)

VmaxC3 (mmole/h/kg)
74421
74421
A-EST oxon-to-TCP (blood)
Km4 (mmol/l)

VmaxC4 (mmol/h/kg)
57003
57003
Oral absorption parameters
KaS (stomach; hr–1)
KaI (intestine; hr–1)
0.5
0.5
KsI (transfer stomach-intestine/h)
0.5
0.5
Fa (fractional absorption; %)
0.80
0.72
Fixedh
Dermal absorption parameter
Surface area (cm2)
—

Fixedi
Kp (permeability coefﬁcient; cm/h)
—
4.81 E–5
TCP model parameters
Vd (l)

Ke (per h)
0.017
0.017
Plasma protein binding
CPF (%)

CPF-oxon (%)

aThe model parameters were estimated independently and held ﬁxed (ﬁxed),
measured in independent experiments (measured), calculated utilizing mathe-
matical algorithms (calculated ) or estimated by ﬁtting the model to the data
(ﬁtted). Dash indicates that the parameter was not incorporated into the model.
bGearhart et al., 1990 (rat).
Brown et al., 1997 (human).
dAndersen et al., 1987.
ePoulin and Krishnan, 1995.
fMa and Chambers, 1994.
gMortensen et al., 1996.
hNolan et al., 1984 (human); Dow, unpublished data (rat).
iMcDougal et al., 1986.
jSultatos et al., 1984 (data only available for CPF; model assumes binding
is slightly higher for CPF-oxon).
kEstimated by ﬁtting model to data from Figure 2.

48, 72, 96, 120, 144, and 168 h following treatment. In addition to blood, urine
specimens were collected prior to treatment and through 168 h postdosing.
Blood and urine specimens were analyzed for the presence of CPF, CPF-oxon,
and TCP by GC-NCI-MS (Brzak et al., 1998). The LOQ for CPF and
CPF-oxon in blood was 3 nmol/l, whereas the TCP LOQ was determined to be
50 nmol/l. In urine specimens, the LOQ for CPF and CPF-oxon was 3 or 3.5
nmol/l and 1 nmol/l for TCP. In addition, blood specimens were centrifuged to
separate plasma from RBC and the inhibition of RBC AChE was determined
as previously described (Ellman et al., 1961). The area-under-the-concentra-
tion curve (AUC0–a) for blood and urinary TCP excretion were determined
using the trapezoidal rule (Renwick, 1994) and the extent of absorption was
calculated based on the amount of TCP recovered in the urine, as described by
Nolan et al. (1984).
RESULTS
Pharmacokinetics/pharmacodynamics of CPF in the rat.
All animals survived the single acute oral administration of
CPF at doses ranging from 0.5 to 100 mg/kg, and the time
course of CPF in the blood and model prediction is presented
in Figure 3. CPF was quantiﬁable at all 6 time points, only for
those animals administered the 100 mg/kg dose, while none of
the blood samples from the 0.5-mg/kg treatment group had
quantiﬁable levels of CPF. This limited kinetic data suggests
that CPF was rapidly absorbed and metabolized with peak
blood levels being observed by 3 h postdosing. The blood-CPF
AUC0–a was calculated as 0.4, 1.1, 5.0, and 12.5 mmol/h/l and
was essentially proportional to dose at all levels. However, at
the highest dose tested (100 mg/kg), there was a small devia-
tion from proportionality that was primarily associated with a
slightly higher observed blood concentration of CPF at 12 h
postdosing. The limited number of quantiﬁable blood samples
over the dose range evaluated made it difﬁcult to adequately
model these data. Initially, CPF uptake was modeled utilizing
a single 1st-order process, which resulted in a much more rapid
rise to peak concentrations than the data suggested. Therefore,
to better describe the absorption of CPF following oral admin-
istration from a corn oil vehicle, a two-compartment gastroin-
FIG. 2.
Experimental data (symbols) and simulations (lines) for the inhi-
bition of plasma ChE in F344 rats administered CPF by oral gavage at dose
levels of 0.5 (open circle), 1 (open square), 5 (open diamond), 10 (ﬁlled circle),
50 (ﬁlled triangle) and 100 mg/kg (ﬁlled diamond). The data represent the
mean 6 SD of 4 animals per treatment group. (Note: the data through 12 h
postdosing was obtained in male rats, whereas the 24 h postdosing data point
was obtained in females).
TABLE 2
Parameters Used in the Pharmacodynamic Model for CPF-oxon
Inhibition of AChE, BuChE and CaE
Parameter
Rat
Human
Estimation Methoda
Enzyme Turnover Rate
(Enz. Hydro./hr–1)
AChE
1.17 E17
1.17 E17
BuChE
3.66 E16
3.66 E16
CaE
1.09 E15
1.09 E15
Enzyme Activity
(mmole/kg/hr–1)
Brain AChE
4.4 E15
4.4 E15
Diaphragm AChE
7.74 E14
7.74 E14
Liver AChE
1.02 E14
1.02 E14
Plasma AChE
1.32 E14
—
Brain BuChE
4.68 E14
4.68 E14
Diaphragm BuChE
2.64 E14
2.64 E14
Liver BuChE
3.0 E14
3.0 E14
Plasma BuChE
1.56 E14
1.73 E16
Fixedb/Fittedg
Brain CaE
6.0 E13
6.0 E13
Diaphragm CaE
3.18 E15
3.18 E15
Liver CaE
1.94 E16
1.94 E16
Plasma CaE
4.56 E15
4.56 E15
Enzyme Degradation Rate
(hr–1)
Kd1 Brain AChE
Kd2 Diaphragm AChE
Kd3 Liver AChE
0.1
0.1
Kd4 Plasma AChE
0.1
—
Kd5 RBC AChE
0.008
0.0008
Kd6 Brain BuChE
Kd7 Diaphragm BuChE
Kd8 Liver BuChE
0.1
0.1
Kd9 Plasma BuChE
0.1
4.2 E–3
Fixedc/Fitted
Kd10 Brain CaE
7.54 E–4
7.54 E–4
Kd11 Diaphragm CaE
Kd12 Liver CaE
Kd13 Plasma CaE
0.0033
0.0033
Bimolecular Inhibition Rate
(mM hr)–1
Ki1-4 All Tissues AChE

Fittede
Ki5 RBC AChE

Fittedi
Ki6-9 All Tissues BuChE

Ki10 Brain CaE

Ki11 Diaphragm CaE

Ki12 Liver CaE

Ki13 Plasma CaE

Reactivation Rate (hr–1)
Kr1-4 AChE
Kr5 RBC AChE
4.0 E–2
4.0 E–2
Kr6-9 BuChE
1.43 E–3
Fixedd/Fittedl
Kr10-13 CaE
Aging Rate (hr–1)
Ka1-5 AChE
Ka6-9 BuChE
Ka10-13 CaE
RBC life-span (days)

Fixedh
aThe model parameters were estimated independently and held ﬁxed (ﬁxed),
measured in independent experiments (measured), or estimated by ﬁtting the
model to the data (ﬁtted). Dash indicates that the parameter was not incorpo-
rated into the model.
bMaxwell et al. 1987.
cGearhart et al. 1990, (rat).
dCarr and Chambers 1996.
eEstimated by ﬁtting model to data from Figure 4.
fEstimated by ﬁtting model to data on CaE inhibition from Chanda et al., 1997.
gEstimated by ﬁtting model to data from Figure 8.
hSchalm 1961.
iEstimated by ﬁtting model to data from Figure 10.
jEstimated based on RBC life-span.
kEstimated by ﬁtting model to Zheng et al., 2000 and data from Table 4.
lEstimated by ﬁtting model to human oral data in Figure 7.

---CHUNK_BREAK---

data from Table 4. lEstimated by ﬁtting model to human oral data in Figure 7. testinal (GI) tract model was utilized as previously described
(Staats et al., 1991). Although this clearly improved the overall
ﬁt, the model did underestimate the peak (3 h) blood CPF
concentration for all treatment groups. Blood specimens were
also analyzed for the presence of CPF-oxon, which was only
detectable in a few of the samples obtained from rats admin-
istered doses greater than 10 mg/kg. In general, the concentra-
tion of CPF-oxon in the blood, when detectable, had a concen-
tration that ranged from 2–7 nmol/l (data not shown) which is
;50–1403 less than the observed CPF concentration in these
same samples (100–1000 nmol/l). Although it was feasible to
identify CPF-oxon in the blood, the observed results were very
close to the analytical limits of quantitation, which likely
contributed to the highly variable response observed. This
variable response and the limited number of quantiﬁable sam-
ples made it particularly difﬁcult to adequately model the
CPF-oxon pharmacokinetics. However, over the dose range
evaluated, the model predicted that the observed CPF-oxon
concentrations ranged from 3 to 36 nmol/l blood (data not
shown), which, although slightly higher than the measured
concentrations, were reasonably comparative given the limita-
tions of the data.
To adequately describe the CPF-oxon stoichiometric inhibi-
tion of both target (i.e., AChE) and nontarget B-EST (i.e.,
BuChE, and CaE), the amount of CaE, BuChE, and AChE
were calculated for the liver, plasma, RBC, brain, and dia-
phragm compartments (See Fig. 1). As previously noted, the
total number of available B-EST binding sites in the various
tissues were based on a previous study conducted in rats
(Maxwell et al., 1987). The authors reported an overall tissue
B-EST ratio of AChE:BuChE:CaE to be 1:2:2051, which in-
dicates that the overall number of CaE binding sites far exceeds
the number of sites available for either AChE or BuChE
binding in the rat. However, Maxwell et al. (1987) also noted
that between tissues there were clear differences in the distri-
bution of B-EST enzymes. Although the plasma ChE in rat
contains appreciable amounts of both AChE and BuChE
(ORNL, 2000), in humans the plasma is devoid of AChE
enzyme (Ecobichon and Comeau, 1973); therefore, only
BuChE and CaE enzyme activity were incorporated into the
PBPK/PD model describing the plasma esterase in humans.
Although reasonable initial parameters were obtainable from
the literature for CPF-oxon inhibition of AChE and BuChE,
experimentally determined parameters were not available for
CPF-oxon inhibition of CaE. To address this deﬁciency the
AChE model parameters were utilized as a starting point. It has
previously been demonstrated that the sensitivity of esterases
to OP inhibition, based on experimentally determined Ki val-
ues for DFP, followed the order: BuChE .. AChE . CaE
(Gearhart et al., 1990). Similarly, Amitai et al. (1998) reported
that CPF-oxon had a much larger Ki for BuChE than AChE in
both rodents and humans (Ki ;100,000 and 581 mM/h, re-
spectively). Since a Ki for CaE inhibition was not available for
CPF-oxon, an apparent Ki was estimated to be 20 mM/h based
on the ratio of Ki’s for AChE and CaE reported by Gearhart et
al. (1990). Hence, for all model simulations the Ki for CaE
inhibition was held constant at 20 mM/h, and only the enzyme
degradation rates (Kd) were optimized to ﬁt the CaE inhibition
data reported by Chanda et al. (1997). The CaE model param-
eters were then held constant for all remaining model simula-
tions (data not shown).
The time course of plasma ChE and brain AChE inhibition
were also determined in rats through 24 h of postdosing fol-
lowing single oral gavage administration of CPF at doses
ranging from 0.5 to 100 mg/kg, and the experimental results
and model simulations are illustrated in Figures 2 and 4. In
these experiments, CPF produced a dose-dependent reduction
in both plasma ChE and brain AChE activity. As might be
expected at any given dose, plasma esterase was inhibited to a
greater extent than brain. The maximum inhibition of plasma
FIG. 3.
and simulations (lines) for the concentra-
tion of CPF in the blood of F344 rats
administered CPF by oral gavage at dose
levels of (A) 50 (triangle) and 100 mg/kg
(square), (B) 5 (diamond), and 10 mg/kg
(circle). The data represent the mean 6
SD of 4 animals per treatment group.
FIG. 4.
Experimental data (symbols) and simulations (lines) for the inhi-
bition of brain AChE in F344 rats administered CPF by oral gavage at dose
levels of 0.5–5 (ﬁlled circle), 10 (ﬁlled triangle) 50 (ﬁlled square) and 100
mg/kg (ﬁlled diamond). The data represent the mean 6 SD of 4 animals per
treatment group. (Note: the data through 12 h postdosing was obtained in male
rats, whereas, the 24 h postdosing data point was obtained in females)

---CHUNK_BREAK---

obtained in male rats, whereas, the 24 h postdosing data point was obtained in females) ChE was observed at 3 to 6 h after the 0.5 to 10 mg/kg doses,
and 3 to 12 h after the 50 and 100 mg/kg doses; doses of 50
mg/kg or greater resulted in a maximum inhibition of plasma
ChE (;90%). Inhibition of brain AChE occurred at dose levels
of 10 mg/kg and higher. Maximum inhibition of brain AChE
occurred from 6 to 12 h postdosing at doses of 10 and 50
mg/kg, and at 3 to 12 h after the 100-mg/kg dose.
The DFP PBPK/PD model developed by Gearhart et al.
(1990) estimated the rate of plasma ChE and brain AChE
synthesis and degradation by model optimization against DFP
experimental data sets, and their optimum Kd’s ranged from
0.01 to 0.1 per h in mice and rats. These synthesis and degra-
dation parameter estimates were likewise used in the current
model. Amitai et al. (1998) determined the in vitro Ki value for
CPF-oxon binding kinetics with puriﬁed AChE and BuChE
enzymes to be ;48,000, 471, and 228 (mM/h) for plasma
BuChE, plasma AChE, and RBC AChE, respectively. How-
ever, utilizing these Ki parameters in the model overestimated
the extent of plasma BuChE and AChE inhibition kinetics (data
not shown); therefore, the in vitro Ki’s were reduced to an
apparent in vivo Ki to better describe the data (see Table 2). By
establishing an apparent Ki for BuChE and AChE enzyme
activity, the PBPK/PD model reasonably simulated the dose-
dependent inhibition of both the plasma ChE and brain AChE
inhibition kinetics over the broad dose range evaluated through
24 h postdosing. The model accurately reﬂected the overall
trends associated with plasma ChE and brain AChE inhibition
kinetics in the rat, and in particular reﬂected the large increase
in enzyme inhibition at doses of 5 and 50 mg/kg in the plasma
and brain, respectively.
The extent of RBC AChE inhibition was likewise deter-
mined at 24 h postdosing in rats orally administered CPF at
single doses ranging from 0.5 to 100 mg/kg. In addition, single
dose RBC AChE inhibition data (4 h postdosing) at doses
ranging from 0.15 to 15 mg/kg was obtained from Zheng et al.
(2000). The resulting inhibition and model-simulated predic-
tion of the enzyme inhibition at 4 and 24 h postdosing are
presented in Table 3. The inhibition of the RBC AChE activity
was dose-dependent; however the RBC’s were less sensitive to
inhibition than plasma ChE, and a no-effect level was seen at
doses of 1 mg/kg or less. The apparent Ki for the RBC’s was
less than for plasma AChE (;100 vs. 243 mM/h, respectively),
and the reactivation rate (Kr) was set at 0.04/h to accommodate
a faster reactivation, through 24 h postdosing, that could not be
accounted for by RBC resynthesis alone. With these parame-
ters, the model dose response was consistent with the experi-
mental data, although the model slightly underpredicted the
peak 4-h inhibition (pred/obs ratios 0.94–2.07), while slightly
overpredicting the 24 h postdosing data (pred/obs ratios 0.34–
0.94). Overall, the model predictions were generally within a
factor of 2 of the experimental data.
Model predictions of effects of repeated dietary doses on
CPF in the rat.
The PBPK/PD rat model was developed from
literature citations and from ﬁtting the data from single-dose
studies. The unaltered model was used to predict the effects of
repeated daily exposure to CPF in the diet. Since the majority
of long-term toxicity testing with CPF has been conducted by
continuously exposing rodents to CPF via the diet, the model
incorporated a dietary exposure regimen. The results of the
TABLE 3
Experimental Data (Observed) and Simulations (Predicted) for Red Blood Cell Acetylcholinesterase (RBC AChE) Measured
at 4 and 24 h Postdosing following Oral Administration in Sprague-Dawley and F344 Rats
Dose
(mg/kg)
4 h Postdosing
24 h Postdosing
% Control
Ratio
predicted/
observed
% Control
Ratio
predicted/
observed
Observed
Predicted
Observed
Predicted
0.15

98.8
0.98
ND
ND
—
0.45

96.5
0.97
ND
ND
—
0.75

94.1
0.94
102.9 6 10.87
95.8
0.93

ND
ND
—
97.3 6 8.87
91.8
0.94
1.5

88.6
1.30
ND
ND
—
4.5

69.7
1.29
ND
ND
—

ND
ND
—
82.8 6 12.0
69.2
0.84
7.5

54.9
2.03
ND
ND
—

ND
ND
—
70.7 6 10.0
54.2
0.77

31.0
2.07
ND
ND
—

ND
ND
—
48.1 6 9.01
26.1
0.54

ND
ND
—
49.2 6 8.8
16.8
0.34
Note. ND, not determined; 4-h postdosing data extracted from Zheng et al., 2000; 24-h postdosing data determined experimentally; n 5 6 animals/treatment
group. Experimentally determined data are given as mean 6 SD.

---CHUNK_BREAK---

experimentally; n 5 6 animals/treatment group. Experimentally determined data are given as mean 6 SD. repeated CPF dietary dosing model simulations on rat brain
AChE, RBC AChE, and plasma ChE inhibition in comparison
to experimental results obtained following 7 to 13 weeks of
dietary CPF administration (Yano et al., 2000) are presented in
Figure 5. The model simulation suggested that a steady-state
level of enzyme inhibition was rapidly attained by 3 to 4 days
following initiation of dosing, although the brain AChE inhi-
bition at the highest dose (15 mg/kg/day) appears to continue
to decline through 30 days of exposure. The model also indi-
cated a dose-dependent inhibition in all tissues with the order
of magnitude of inhibition as follows: plasma . RBC . brain.
Following a 0.1 mg/kg/day dose of CPF, the PBPK/PD model
accurately described the lack of brain (100% of control), and
RBC AChE inhibition (;98% of control) and minimal plasma
ChE inhibition (;96% of control). The model also predicted
the lack of brain AChE inhibition (100% of control) and slight
RBC AChE inhibition (;80% of control) following exposure
to a 1 mg CPF/kg/day dose. However, the model underesti-
mated the extent of plasma ChE (;75% of control) inhibition
relative to the experimental results (46% of control). Simulat-
ing a continuous dose of 5 mg/kg/day, the model also under-
predicted the plasma ChE (;50% vs. 23% of control), and
brain AChE inhibition kinetics (;80% vs. 55% of control)
relative to the experimental data, but reasonably estimated
RBC AChE (;50% vs. 55% of control) inhibition. Finally,
following a repeated dietary exposure to 15 mg CPF/kg/day,
the model reasonably estimated the extent of plasma ChE
(;25% vs. 19% of control), brain AChE (;38% vs. 54% of
control), and RBC AChE inhibition (;30% vs. 38% of control)
kinetics. The model response suggested that, at doses $ 5 mg
CPF/kg/day, the CPF-oxon concentration in the brain attained
an adequate concentration to overwhelm available detoxiﬁca-
tion pathways resulting in signiﬁcant brain AChE inhibition.
The experimental data of Yano et al. (2000) is consistent with
the model simulations, but slight quantitative differences sug-
gest that detoxiﬁcation pathways may be overwhelmed at
lower doses (i.e., between 1 and 5 mg/kg/day) than the current
PBPK/PD model predicts. It is conceivable that matrix effects
associated with corn oil vs. dietary dose preparation and ad-
ministration could result in variable oral bioavailability, which
would effectively shift the dose response. To adequately ad-
dress this question, additional pharmacokinetic/pharmacody-
namic studies are needed to determine target tissue dosimetry
and dynamic response following chronic dietary exposure to
CPF. Nonetheless, until additional data is available, the
PBPK/PD model provides a reasonable qualitative assessment
of the dose-dependent pharmacodynamic response that is ob-
served in rats following chronic dietary administration of CPF.
Pharmacokinetics/pharmacodynamics of CPF in humans.
The rodent PBPK/PD model was extended to incorporate hu-
man physiological constants, and the metabolic parameters
were appropriately scaled as a function of body weight to
enable the model to describe CPF dosimetry and dynamic
response in humans. When available, parameters derived for
human studies (in vitro/in vivo) were utilized in the model.
Speciﬁcally, since human plasma ChE activity is primarily
associated with a higher amount of BuChE vs. AChE (Ecobi-
chon and Comeau, 1973) relative to the enzyme levels in
rodent plasma, the amount of BuChE enzyme in the model of
human plasma was increased (see Table 2) based on available
data (Chan et al., 1994). Nolan et al. (1984) conducted a
controlled human study where volunteers were administered
single doses of CPF orally (0.5 mg/kg) as well as dermally (5
mg/kg) and the pharmacokinetic and pharmacodynamic re-
sponses were then determined. This data set was utilized to
calculate the appropriate elimination rate constant (Ke) and
volume of distribution (Vd) to accurately describe the pharma-
FIG. 5.
Model simulation of ChE in-
hibition in plasma (A), brain AChE (B),
and RBC AChE (C) in F344 rats follow-
ing dietary administration of CPF for
;30 days at doses of 0.1, 1, 5, and 15
mg/kg/day. The plasma, RBC and brain
table insert (D) represents experimental
data from Yano et al. (2000), obtained
following 7 to 13 weeks of repeated di-
etary exposure to CPF.

---CHUNK_BREAK---

al. (2000), obtained following 7 to 13 weeks of repeated di- etary exposure to CPF. cokinetics of TCP, and the dermal permeability coefﬁcient
(Kp) that was capable of accurately describing the extent and
rate of dermal uptake of CPF. Secondly, the plasma BuChE
enzyme activity and reactivation rate was optimized against the
plasma BuChE inhibition data obtained following the single
0.5 mg CPF/kg oral dose. These model parameters were then
held constant and model simulations were run against human
pharmacokinetic data obtained within this study, and against
limited
pharmacokinetic
data
available
in
the
literature
(Drevenkar et al., 1993).
Nolan et al. (1984) reported that the blood CPF concentra-
tions following either oral or dermal exposure were extremely
low (,0.085 nmol/ml) and exhibited no consistent temporal
pattern; however the levels of the major metabolite TCP were
readily quantiﬁable in both blood and urine following either
dermal or oral administration. Therefore, the PBPK/PD model
was used to characterize the TCP pharmacokinetics. Based on
the amount of TCP excreted in the urine, it was determined that
70% 6 11 and 1.28% 6 0.83 of the oral and dermal dose of
CPF was absorbed in these volunteers, respectively (Nolan et
al., 1984). The time course of TCP in the blood and urine of
these human volunteers, and the resulting model simulations
following either a single oral 0.5-mg/kg or a dermal 5 mg/kg
dose of CPF are presented in Figure 6. Following the oral or
dermal dose, peak plasma TCP concentrations were 4.69 and
0.44 mmol/l and were attained at both 5 and 24 h postdosing.
In addition, peak TCP urine excretion was achieved by 24 h
postdosing for both the oral and dermal treatments, and the
time course of urine excretion was very comparable for both
dosing routes. Overall, the model provided a reasonable pre-
diction of the route-dependent blood TCP kinetics following
CPF exposure in humans.
Unlike the simple one-compartment model utilized to de-
scribe the fractional absorption of CPF in humans (Nolan et al.,
1984), the PBPK/PD model was modiﬁed to calculate the ﬂux
of CPF through the skin as a function of CPF permeability,
concentration, area of exposed skin surface, and exposure
length (Poet, 2000). Hence, the PBPK/PD model calculated a
permeability coefﬁcient (Kp) of 4.81 3 10
–5 cm/h, and as-
sumed a dermal exposure not exceeding 20 h postapplication;
the estimated fractional absorption was 2.32%. This result is
similar to the 1.28% and ;1% dermal absorption based on the
recovery of TCP and dialkylphosphate metabolites in the urine,
respectively (Nolan et al., 1984; Grifﬁn et al., 1999). The time
course of plasma BuChE inhibition kinetics following a single
oral (0.5 mg/kg) or dermal (5 mg/kg) dose of CPF in human
volunteers is presented in Figure 7. As previously noted, the
amount of available plasma BuChE enzyme and the rate of
enzyme recovery were optimized to ﬁt the plasma BuChE
inhibition time course following the oral 0.5 mg/kg CPF dose.
The model parameters determined from the oral dosing study
were then held constant and the PBPK/PD model was used to
predict the extent of plasma BuChE inhibition following a 5
mg CPF/kg dermal exposure. Under this dermal exposure
scenario, the model predicted maximum plasma BuChE inhi-
bition of ;90% of control, which was comparable to the
observed 87% seen with the experimental data; likewise the
model reasonably predicted the enzyme recovery kinetics
through 200 h postdosing.
Model predictions of effects of single, oral doses of CPF in
human males and females.
The model parameters for humans
were derived from the literature and from ﬁtting data from
Nolan et al. (1984). Without altering the model parameters, the
results of the controlled human CPF pharmacokinetic study,
conducted as part of this project, were also compared against
the PBPK/PD model predictions. There were no differences
observed in the concentrations or time course of CPF and
metabolites in these volunteers that was attributable to gender
(data not shown). Following oral administration of CPF at
doses ranging from 0.5 to 2 mg/kg, only 5 of the 12 volunteers
FIG. 6.
from Nolan et al. (1984) and model sim-
ulations (lines) of the TCP pharmacoki-
netics in human volunteers administered
an oral dose of 0.5 mg CPF/kg or a
dermal dose of 5 mg CPF/kg. The time
course data of TCP in the blood (A)
represents the mean 6 SD for 6 (oral)
and 5 (dermal) male volunteers; (B) the
amount of TCP excreted in the urine
from the same volunteers.
FIG. 7.
Experimental data (symbols) from Nolan et al. (1984) and model
simulations (lines) of the plasma ChE inhibition in human volunteers admin-
istered an oral dose (ﬁlled circles) of 0.5 mg CPF/kg or a dermal dose (ﬁlled
squares) of 5 mg CPF/kg. The time course data represents the mean 6 SD for
5 male volunteers.

on the study had quantiﬁable levels of CPF detected in a
limited number of blood specimens and no CPF-oxon was
detected in any specimens (LOQ 5 3 nmol/l). The time course
and model simulations of CPF and TCP concentrations in the
blood of 5 volunteers (A–E) orally administered CPF at doses
of 1 or 2 mg/kg are presented in Figure 8. Only one individual
in this study, administered a dose of 2 mg CPF/kg, exhibited
any RBC AChE inhibition (Volunteer E). The experimental
data and model simulations indicate that CPF blood concen-
trations were at least 2 orders of magnitude less than the
observed TCP blood concentrations, and all the blood speci-
mens taken after 8 h postdosing were below quantitation limits
for CPF. The model simulation was consistent with a rapid
metabolic clearance of CPF, resulting in the formation of TCP,
which had a considerably slower elimination rate and was
readily detectable in the blood of these volunteers through
160 h post-dosing. Based on the model ﬁt of these experimen-
tal data, the extent of oral absorption for these 5 volunteers
ranged from ;18% to 38%, which is considerably less that the
oral bioavailability of the 70% previously calculated for human
volunteers, using a one-compartment model (Nolan et al.,
1984). The observed differences in oral bioavailability in these
2 studies are most likely associated with differences in dosage
formulation (i.e., tablet vs. capsule).
Urine specimens were likewise analyzed for CPF, CPF-
oxon, and TCP; however, neither CPF nor CPF-oxon was
detected in any of the samples. The average TCP blood con-
centration and urine excretion time course for all human vol-
unteers (male and female) administered 0.5, 1, or 2 mg CPF/kg
as single oral doses are presented in Figure 9. Over the dose
range evaluated, the kinetics of TCP in blood and urine were
linear and proportional to dose. However, the model-predicted
average oral fractional absorption for all treatment groups was
;20% of the orally administered dose, which was very close to
the AUC0–a estimation of 22.4% absorption of administered
dose made from the TCP measurements in urine.
FIG. 8.
and model simulations (lines) for the
plasma concentration of TCP (ﬁlled cir-
cles) and CPF (ﬁlled squares) in 5 vol-
unteers administered CPF as an oral dose
of 1 mg/kg (A and B) or 2 mg/kg (C, D,
and E). A–E, the individual results from
the 5 volunteers.
FIG. 9.
and model simulations (lines) of the TCP
pharmacokinetics in human volunteers
administered oral doses of 0.5 (ﬁlled di-
amonds), 1 (ﬁlled triangles), and 2 (ﬁlled
circles) mg CPF/kg. The time course data
of TCP in the blood (A) represents the
mean 6 SD for 12 male/female volun-
teers; (B) the amount of TCP excreted in
the urine is from the same volunteers.

---CHUNK_BREAK---

teers; (B) the amount of TCP excreted in the urine is from the same volunteers. The impact of single oral CPF doses (0.5, 1, or 2 mg/kg) on
RBC AChE activity was assessed in these same human volun-
teers, and the results are presented in Figure 10. There was no
inhibition of RBC AChE in males at any dose level (Fig. 10A).
There was a slight decrease in RBC AChE activity in females,
beginning at 8 h postdosing at the 2 mg/kg dose level (Fig.
10B). The decrease in RBC AChE activity appeared to be due
to inhibition in one volunteer (Fig. 10C, Volunteer E). When
data from the single volunteer was removed from the data set,
the average RBC AChE activity in the remaining women (n 5
5) was virtually indistinguishable from baseline.
Although the oral dose of CPF was 2 mg/kg body weight,
the amount absorbed was appreciably less. For the 6 men and
5 women that had no RBC AChE inhibition, the urinary TCP
AUC0–a, when corrected for average body weight, was com-
parable across gender at 2.97 and 2.78 mg/h/kg, respectively.
Given an absorbed fraction of 0.70 of CPF that is recovered in
urine as TCP (Nolan et al., 1984), the estimated average
absorbed dose of CPF was 0.57 mg/kg. The woman with
inhibited RBC AChE had about 2 times more TCP recovered
from the urine (TCP AUC0–a, 5.55 mg/h/kg), which repre-
sented an estimated absorbed dose of 1.1 mg/kg of CPF. The
model made a reasonable prediction of both the timing and
degree of human RBC AChE activity for the woman with high
absorption of CPF, and predicted little or no inhibition of the
other 5 women that had less absorption (Fig. 10C).
Although only limited CPF blood time course data was
available from the controlled human exposure (see Fig. 8) the
model was capable of accurately describing the CPF blood
kinetics. To further validate the capability of the model to
accurately describe the pharmacokinetics of CPF, the time
course of CPF in serum from an individual who ingested a
concentrated formulation of CPF (Drevenkar et al., 1993) was
modeled and the results are presented in Figure 11. The subject
was a 25-year-old male reported to have drunk 30–60 ml of a
commercially available insecticide that contained CPF as the
active ingredient. The subject was admitted to the hospital 2 to
5 h after ingestion of the pesticide formulation, and CPF was
quantitated in the serum for up to 15 days after poisoning. The
samples were likewise analyzed for CPF-oxon; however the
FIG. 10.
RBC AChE activity in male (A) and female (B) volunteers presented as the mean 6 SD for 6 volunteers administered CPF doses of 0 (Control),
0.5, 1, or 2 mg/kg of body weight, and the average control normalized RBC AChE activity (C) for the female 2-mg/kg treatments, with and without the inclusion
of a single individual who was a high absorber. The symbols represent the observed data, while the line represents the model simulation. (Note: This study was
conducted in two parts. Part 1 included control 1, 0.5, and 1 mg/kg doses; Part 2 included control 2 and 2 mg/kg dose).

---CHUNK_BREAK---

1, 0.5, and 1 mg/kg doses; Part 2 included control 2 and 2 mg/kg dose). oxon was not detectable in any of the samples (Drevenkar et
al., 1993). The PBPK/PD model was capable of accurately
describing the overall pharmacokinetics of CPF in the blood
following a single acute exposure. Based on the observed CPF
blood time course, the model estimated that an acutely toxic
dose of ;180 mg/kg was needed to achieve the highest con-
centrations of CPF (1–10 mmol/l) that were detected in the
serum. This predicted dosage is well within the range of
reported acute LD50 doses (85–504 mg/kg) in animals, and is a
reasonably good approximation of a dosage that is capable of
producing the reported acute toxicological responses in hu-
mans (Gaines 1969; McCollister et al., 1974).
DISCUSSION
Thionophosphorus organophosphates such as CPF constitute
a large class of chemical insecticides that have seen widespread
utilization in both agriculture and home applications. The
potential for OP insecticides to produce a toxic response is
dependent upon the balance between the amount of delivered
dose to the target site and the rates of bioactivation and/or
detoxiﬁcation (Calabrese, 1991). In order to quantitatively
integrate all the physiological, metabolic, and biochemical
factors associated with CPF absorption, distribution, metabo-
lism to CPF-oxon and TCP, and the resulting ChE inhibition,
a PBPK/PD model was developed for both rats and humans.
Overall, the results presented here illustrate that the current
model can reasonably describe rat and human dosimetry and
dynamic response data under a broad range of exposure sce-
narios (acute vs. chronic, oral vs. dermal). However, it is also
recognized that some model ﬁts could be improved upon,
which supports the need for additional experimental data,
including better parameter estimates, to facilitate future model
reﬁnement.
In developing the CPF model it became obvious that, al-
though a considerable amount of hazard evaluation research
has been performed on CPF, only a limited number of phar-
macokinetic studies were available for model development.
Therefore, both rat and human pharmacokinetic/pharmacody-
namic studies were conducted to provide the needed experi-
mental data to develop and validate the model. Utilizing re-
cently developed sensitive (i.e., low ppb range) analytical
methods (Brzak et al., 1998) it was feasible to quantitate CPF,
CPF-oxon, and TCP following in vivo exposures to CPF and to
directly link dosimetry with the observed ChE and AChE
inhibition kinetics in both rats and humans.
The PBPK/PD model provides important insights into the
route- and dose formulation-dependent absorption of CPF in
rats and humans. Due to its poor aqueous solubility, CPF dose
solutions are generally prepared in an oil-based matrix (e.g.,
corn oil) and administered to rodents by oral gavage. Previous
studies have shown that the dosing vehicle can modify the
amount and rate of absorption, and corn oil in particular has
been shown to result in lower peak and increased time to
maximum blood concentrations (Cmax) (Withey et al., 1983).
Hence, to describe the uptake of CPF from the GI tract of rats,
we needed a two-compartment GI tract model similar to the
one used to describe the uptake of chlorinated solvents (Staats
et al., 1991). This model modiﬁcation resulted in a more
accurate simulation of CPF uptake than was feasible with the
single-compartment model, although it did not enable the
model to adequately ﬁt the peak blood (3 h postdosing) CPF
concentration. In addition to a slower overall rate of uptake,
due to corn oil, the amount of CPF orally absorbed in rats was
estimated to be ;80%. This estimate was based on pharma-
cokinetic studies where rats were administered
14C-labeled
CPF and the
14C activity was determined in tissues and excreta
(Dow Chemical, unpublished report). Differences in the extent
of CPF absorption were also clearly evident when comparing
the human CPF pharmacokinetics conducted in this study with
the results from human kinetic studies conducted under differ-
ent dosing conditions. Nolan et al. (1984) deposited a known
amount of CPF onto a lactose tablet, which was subsequently
swallowed with water. This dose preparation resulted in ;70%
of the orally administered dose being recovered as TCP. In
contrast, the CPF dose in the current human kinetic study was
prepared by adding CPF and lactose as dry powders into a
dissolvable capsule that was likewise swallowed with water,
however only 20–35% of this oral dose was recovered as TCP.
Based on these experimental ﬁndings, the extent of CPF ab-
sorption appears to be dependent upon its physical form when
administered. The question of bioavailability is of particular
importance when interpreting a ChE response based only upon
the administered dose, without taking into full consideration
how much of that dose was actually absorbed. Therefore,
interpretation of pharmacodynamic response data would cer-
tainly be strengthened with a concurrent assessment of bio-
availability within the same study. This analysis could readily
be accomplished by quantitating blood or urinary TCP concen-
trations. However, for the purposes of the rat PBPK/PD model
development, the oral absorption of CPF, using a corn oil
dosing matrix, was set at 80% for all model simulations. This
assumption was made while fully recognizing that it represents
FIG. 11.
Time course of CPF in serum of a single poison victim that orally
ingested a commercial insecticide product containing CPF (data extracted from
Drevenkar et al., 1993). The symbols represent the observed data while the line
represents the model simulation.

---CHUNK_BREAK---

al., 1993). The symbols represent the observed data while the line represents the model simulation. an oversimpliﬁcation, since the extent of absorption can be
drastically different depending on the conditions of the dose
solution (i.e., formulation), dosing method, and variations in
species, gender, or strain (Kararli, 1995).
In reality the majority of both occupational and environmen-
tal exposures to OPs are primarily associated with the dermal
route, which has been reported to account for more than 90%
of the systemically absorbed dose in humans (Aprea et al.,
1994). Therefore, an understanding of percutaneous absorption
of OPs is critical for quantitatively determining a systemic
dose. The extent of in vivo dermal absorption of CPF in
humans has previously been reported as low (1–3%; Grifﬁn et
al., 1999; Nolan et al., 1984). This is consistent with the low in
vivo dermal absorption potential reported in humans exposed to
diazinon, isofenphos, and malathion, which ranged from 2.5–
3.9% of the applied dose (Wester et al., 1983; 1992; 1993). In
the current PBPK/PD model, the dermal uptake of CPF in
humans was well described by estimating a CPF permeability
coefﬁcient (Kp) of 4.81 3 10
–5/cm/h utilizing previously pub-
lished dermal absorption data in humans (Nolan et al., 1984).
The model presented herein quantitatively predicts the concen-
tration of CPF, CPF-oxon, and TCP in blood, tissues, and
excreta in both rats, and humans following exposure, either
orally or through direct skin contact, with CPF. These results
are consistent with TCP being the major metabolite formed that
attained a blood concentration of 100-fold higher than the
parent compound (see Fig. 8). Likewise, the pharmacokinetic
studies conducted in rats suggest that levels of CPF in the
blood exceed the CPF-oxon concentrations. These results
clearly indicate that even when employing sensitive analytical
techniques, quantiﬁable concentrations of both CPF and CPF-
oxon in blood are only obtainable when relatively high doses of
CPF (.5 mg/kg) were administered, and even then, it was only
detectable for a limited time after dosing. This inability to
adequately quantitate both CPF and CPF-oxon blood concen-
trations over a range of dose levels has made it particularly
challenging to accurately model dosimetry, particularly at low
doses (,10 mg/kg).
Biomonitoring of OPs and their metabolites in blood and
urine has been used to provide a quantitative assessment of
dosimetry in human poison victims following acute high-dose
exposure (Drevenkar et al., 1993; Vasilic et al., 1992), and for
the assessment of secondary exposures (Loewenherz et al.,
1997; Richter et al., 1992). A major advantage in utilizing the
analysis of intact pesticide or speciﬁc metabolites in body
ﬂuids versus ChE depressions is that it enables identiﬁcation of
speciﬁc chemical agent(s) that may be associated with the
observed esterase inhibition (Ellenhorn and Barceloux, 1988;
Lotti et al., 1986), and as previously mentioned, can be used to
better determine bioavailabilty. The utilization of PBPK/PD
models such as the one developed for CPF enables the quan-
titative integration of dosimetry with biological response. The
model can predict the extent of esterase inhibition (see Fig. 7)
based on the observed concentrations of either the parent
compound (see Figs. 8 and 11) or metabolites (see Figs. 6, 8,
9). Hence this PBPK/PD model provides an integrated assess-
ment of CPF dosimetry and biological response in both rats and
humans for a number of exposure scenarios.
The PBPK/PD model integrates CPF dosimetry with a phar-
macodynamic model capable of predicting stoichiometric B-
EST inhibition, and is consistent with other pharmacodynamic
models such as the one developed for soman in the rat (Max-
well et al., 1988). The extent and rate of B-EST inhibition and
recovery is dependent upon the amount of available enzyme,
the Ki, and the amount of time the B-EST is exposed to the
available oxon (Vale, 1998). As previously noted, the amount
of available B-EST binding sites (mmol) in general followed
the order CaE .. BuChE ' AChE (Maxwell et al., 1987),
whereas the Ki rates followed the order: BuChE .. AChE .
CaE. Initial model simulations utilized relatively higher Ki
values determined with puriﬁed BuChE and AChE enzyme
(Amitai et al., 1998), which severely over predicted the extent
of ChE and AChE inhibition (data not shown). In this regard,
Mortensen et al. (1998) noted differences in in vitro sensitivity
(i.e., IC50s) of AChE when comparing the inhibition of puriﬁed
enzyme against crude tissue homogenates. Hence it is not
unreasonable to expect that the Ki values determined with
puriﬁed enzymes would not adequately describe the inhibition
response obtained with crude enzyme preparations. Therefore,
an apparent Ki was determined for CPF-oxon inhibition of
B-EST enzymes that was qualitatively consistent with the Ki
values measured with puriﬁed enzymes (Amitai et al., 1998).
The model simulation suggests that BuChE is the most sensi-
tive to CPF-oxon inhibition due to a higher apparent Ki (2.0 3

3 mM/h) and relatively low amounts (;1600 mmol total in
rat) of available BuChE in the tissues. In contrast, the model
predicts that CaE is the least sensitive to CPF-oxon, and
appears to be due to the combination of an estimated low
apparent Ki (20 mM/h), and high amounts of available enzyme
(2 3 10
6 mmol total in rat). Finally, the sensitivity of AChE
enzyme to CPF-oxon inhibition resulted from a moderate (be-
tween BuChE and CaE) apparent Ki (243 mM/h), and rela-
tively low amounts (;1000 mmol total in rat) of available
AChE enzyme. Although these apparent Ki parameter esti-
mates provide a reasonable description of the B-EST inhibition
kinetics, it is clear that the model would be further strength-
ened by experimentally determining these Ki parameters under
physiological conditions that more accurately reﬂect in vivo
activity. In addition, uncertainty associated with model esti-
mates of CPF-oxon concentration raises the possibility that the
model overestimates of CPF-oxon concentration, particularly
at high doses, may have contributed to excessive esterase
inhibition predictions. Additional quantitative data on CPF-
oxon blood and/or tissue concentrations and Ki parameter
estimates may help resolve this question.
Chanda et al. (1997) evaluated the tissue-speciﬁc effects of
CPF on both CaE and ChE, utilizing in vivo and in vitro
comparisons. They reported that the maximum inhibition of

---CHUNK_BREAK---

ChE, utilizing in vivo and in vitro comparisons. They reported that the maximum inhibition of plasma CaE, following an 80-mg CPF/kg dose, was ;40% of
control (Chanda et al., 1997), whereas, in the current study, a
comparable level of plasma ChE (50:50—BuChE: AChE)
inhibition was achieved at a dose level of ;5 mg CPF/kg (see
Fig, 2). These results are consistent with the observed differ-
ences in apparent Ki’s, and the amounts of available B-EST
enzymes in the rat. Likewise, these results are consistent with
the observation that B-EST inhibition is an integrated function
of target-tissue dosimetry, esterase afﬁnity for CPF-oxon, and
the number of available esterase binding sites in each tissue
compartment. In this regard, improvements in the predictive
capability of the current model may be achieved by conducting
studies that better characterize the time course of speciﬁc
esterase activities (i.e., AChE, BuChE, and CaE) in both blood
and tissue compartments over a broad range of CPF exposures.
It has been generally accepted that the biological bases of
risk assessments are strengthened by the utilization of an
internal dose surrogate versus the administered dose in cross-
species extrapolations (Andersen, 1995). A determination of
dose-rate effect may also be important, since under the Food
Quality Protection Act (FQPA) there is concern about the risk
associated with pesticide residue exposures where dermal con-
tact and/or ingestion of low levels of pesticide residue on food
constitute important exposure routes (U.S. EPA, 1998). In this
case, an evaluation of maximum blood concentration (Cmax)
and/or blood AUC is of relevance since these dose surrogates
may be particularly sensitive to dosing rate (Corley, et al.,
1994). To illustrate this point, a simulation of the blood CPF
concentration and plasma ChE response in rats following either
a single bolus dose of 10 mg CPF/kg or the same dose frac-
tionated (3 3 3.3 mg/kg at 8-h intervals) over a 24-h period is
presented in Figure 12. Based on model simulations, the Cmax
for blood CPF was ; 0.05 mmol/l, whereas the same dose
when fractionated over a 24-h period attained a Cmax of ;0.02
mmol/l. Although the blood concentration for the fractionated
dose was slightly less than half of that obtained following the
bolus administration, repetitive dosing did result in the blood
levels of CPF being maintained at elevated levels until dosing
ceased (;24 h). The potential impact of dividing the dose was
particularly evident when comparing the model simulation of
ChE inhibition (see Fig. 12 B). Compared to bolus adminis-
tration, dividing the dose reduced the peak inhibition by ;10%
(;27% of control). These simulations infer that the adminis-
tration of CPF as a large bolus dose, results in a greater
maximum plasma ChE inhibition than when the same dose is
administered over a prolonged time period (i.e., divided).
Based on these model simulations, future studies should con-
sider experimentally determining the impact of dose-rate on
both CPF dosimetry and dynamic response.
Simulations of the AUC0–a for the concentration of CPF in
blood and CPF-oxon in both blood and brain for rats and
humans acutely exposed by oral ingestion to a broad range of
FIG. 12.
Simulated concentration of
CPF in blood (A) and ChE inhibition in
plasma (B) following oral administration
of a single dose of CPF (10 mg/kg), or
the same dose divided (3 3 3.3 mg/kg, at
8-h intervals) over the ﬁrst 24-h interval.

---CHUNK_BREAK---

same dose divided (3 3 3.3 mg/kg, at 8-h intervals) over the ﬁrst 24-h interval. CPF doses (0.001–100 mg/kg) is presented in Figure 13. To
compare the response at equivalent doses between species, the
oral absorption was set at 80%. In both rats and humans, the
AUC0–a followed the order: CPF (blood) . CPF-oxon
(blood) . CPF-oxon (brain). Over the dose range evaluated,
the CPF blood AUC0–a ranged from ;4–13-fold higher in
humans than in rats and demonstrated a slightly increasing
trend with dose. In contrast, at low doses (,1 mg/kg), the
AUC0–a for CPF-oxon (blood and brain) in rats was ;2–4-fold
higher than at comparable doses in humans. However, in
humans, increasing the dose above 1 mg/kg resulted in a
nonlinear “crossover” response so that at high doses the sim-
ulated human AUC0–a for CPF-oxon (blood and brain) ex-
ceeded that of the rat (;1.1–6-fold). Although these simula-
tion results must be evaluated, taking into full consideration the
uncertainty in the model predictions of the CPF and CPF-oxon
concentrations, the simulation is consistent with a response
where one or more of the detoxiﬁcation pathways has become
overwhelmed.
As previously noted, the extent of CYP450 activation of
CPF to CPF-oxon and differences in detoxiﬁcation are most
likely responsible for any observed species-dependent in-
creased sensitivity. Since tissue and blood B-EST stoichiomet-
rically bind to oxon and become irreversibly inactivated (Chan-
dra et al., 1997; Clement, 1984), one reasonable hypothesis is
that the dose-dependent depletion of nontarget B-EST is a key
component contributing to the observed species differences in
the dose response for AChE inhibition. Therefore, by compar-
ing the dose-dependent inhibition of plasma ChE in rats and
humans, it may be possible to illustrate the potential protective
role of nontarget B-EST. However, it is important to recognize
that across species there are marked quantitative differences in
the amount of available B-EST (Ecobichon and Comeau,
1973). For example, as previously noted in rat plasma, ChE is
the sum of both plasma AChE and BuChE activity (Maxwell et
al., 1987), whereas in humans, plasma ChE is exclusively
BuChE (ONRL, 2000). A simulation of the maximum plasma
ChE response in rats and humans, following acute oral expo-
sure to a broad range of CPF doses (0.001 to 100 mg/kg), is
presented in Figure 14. To compare the responses between rats
and humans, at equivalent systemic doses, the oral absorption
was set at 80%. In the model simulation, both rat and human
plasma BuChE have a similar dose response and are essentially
depleted at doses between 1 and 10 mg/kg. However in the rat,
the available plasma AChE enzyme is not depleted until the
dosage is $10 mg/kg. These results are consistent with the
dose-dependent AUC0–a simulations for CPF and CPF-oxon
(see Fig. 13) and suggest a plausible relationship between the
extent of CPF activation, the depletion of nontarget B-EST,
and the nonlinear increase in human CPF-oxon blood and brain
concentration at doses $1 mg/kg. It is important to realize that
in assessing plasma esterase activity, a single substrate, acetyl-
thiocholine (AcTh), is routinely utilized for plasma ChE de-
terminations, although AcTh has a greater speciﬁcity for AChE
than for BuChE enzyme (Venkataraman and Rani, 1994;
ORNL, 2000). This analytical approach has made it particu-
larly challenging to model the rodent esterase response in
compartments, like blood, where both AChE and BuChE en-
zymes are available to CPF-oxon for binding and inhibition.
Therefore, in accessing the protective role of nontarget B-EST
it is important to carefully consider the contribution of multiple
esterases and the importance of enzyme substrate speciﬁcity in
determining enzyme inhibition.
Rat and human data on inhibition of RBC AChE are also
consistent with the PBPK model. The model estimates similar
levels of CPF oxon in the blood of humans and rats, particu-
larly at doses around 0.2 to 0.5 mg/kg (Fig. 13). Based upon
absorbed doses of CPF, humans and rats also had similar
proﬁles of inhibition of RBC AChE. There was no inhibition of
RBC AChE in humans that had an absorbed dose of 0.57
mg/kg, and an absorbed dose of 1.1 mg/kg caused approxi-
mately 25% inhibition in one human volunteer (Fig. 10C). Rats
given an oral gavage dose of 0.75 mg/kg had no inhibition of
RBC AChE, and an oral dose of 1.5 mg/kg caused about 30%
inhibition (4 h postdose, Zheng et al., 2000). Thus, based upon
modeled estimates of blood CPF oxon and RBC AChE inhi-
bition, there appeared to be little difference between rat and
human RBC AChE responses at this dose range.
Although the current PBPK/PD model describes the phar-
FIG. 14.
Simulation of peak plasma total ChE (AChE 1 BuChE), AChE
and BuChE inhibition dose response in rats and humans BuChE following an
acute exposure to a broad range of CPF doses.
FIG. 13.
Simulation of the area under the concentration curve (AUC0–a)
for CPF in blood and CPF-oxon in blood and brain in rats (dashed lines) and
humans (solid lines) following an acute exposure to a broad range of CPF
doses.

---CHUNK_BREAK---

and humans (solid lines) following an acute exposure to a broad range of CPF doses. macokinetics and pharmacodynamics of CPF over a broad dose
range (0.5–100 mg/kg), it is important to recognize that even
the lowest doses evaluated in the current study are still signif-
icantly greater than typical aggregate (total dietary and resi-
dential) human exposures. In both adults and children, poten-
tial aggregate exposures to CPF are estimated to range from
0.46 to 1.7 mg/kg/day, which is ;294- to 1000-fold below the
lowest dose (0.5 mg/kg) used in this study (Gibson et al., 1999;
Hill et al., 1995; Quackenboss et al., 1998; Shurdut et al.,
1998; ). Based upon the observed dose response, where CPF
and CPF-oxon were nondetectable and blood ChE activity was
minimally depressed at doses of 0.5 mg/kg, it is hypothesized
that a signiﬁcant ﬁrst-pass metabolism will be observed at
environmentally relevant doses. In this regard, a number of
recent studies have demonstrated that intestinal epithelial cells
have CYP450 metabolic capacity and are capable of signiﬁ-
cantly altering oral bioavailability of drugs and chemicals in
animals and humans (Hall et al., 1999; Obach et al., 2001;
Paine et al., 1999; Schmiedlin-Ren et al., 1993; Watkins, 1992;
Zhang et al., 1999). A number of the CYP450 isoforms resid-
ing within the intestines have been shown to metabolize a
number of OP insecticides including parathion, diazinon, and
CPF (Butler and Murray, 1997; Fabrizi et al., 1999; Sams et
al., 2000). In addition, P-glycoproteins (multidrug resistance
proteins) are located in the apical borders of intestinal cells,
and are known to be upregulated and bound by CPF-oxon
(Lanning et al., 1996). Thus, an unknown amount of ﬁrst-pass
CPF detoxiﬁcation and activation should occur in the intes-
tines, and CPF-oxon that is generated in enterocytes would be
subject to removal by P-glycoproteins. Since the current model
does not incorporate intestinal metabolism or P-glycoprotein
removal of CPF-oxon, it is anticipated that the model overes-
timates low-dose oral bioavailability, thereby potentially over-
predicting dosimetry and dynamic response. Therefore, to ad-
dress this important question, research is ongoing to further
reﬁne the PBPK/PD model with the inclusion of a metaboli-
cally active intestinal compartment, and associated studies are
being conducted to validate the model response at environmen-
tally relevant exposures.
The PBPK/PD model that was developed for CPF is capable
of quantitating target tissue dosimetry and dynamic response in
both rats and humans, and is a useful tool to quantitatively
assess risk associated with CPF exposure as well as helping to
design and focus future experimental research. The capability
of the model to accurately predict dosimetry and response is
limited by the adequacy of the model parameters and limita-
tions of the experimental data. As with all models, developing
and validating a PBPK/PD model is an iterative process and
highlights the current limitations of our understanding of crit-
ical biological processes that help identify important data gaps.
Additional research could provide a better characterization of
the absorption kinetics and dosimetry for CPF and CPF-oxon
under various dosing conditions. Of particular importance are
experimental data to better understand the extent of CPF ab-
sorption at environmentally relevant exposures, and to evaluate
the potential role of gut metabolism and CPF-oxon protein
binding following low-dose exposures. Additional studies
could better characterize the time course and dose response for
RBC AChE inhibition, since this pharmacodynamic response
is particularly relevant as a potential biomarker for exposure.
Better parameter estimates are needed for the binding of CPF-
oxon with B-EST and in particular the CaE tissue inhibition
kinetic parameters for both rats and humans. In conclusion, this
CPF PBPK/PD model quantitatively estimates target tissue
dosimetry and AChE inhibition, and is an effective framework
for future OP model development, and for establishing a bio-
logically based risk assessment for CPF exposure under a
variety of scenarios.
APPENDIX
Differential equations and abbreviations for the various tissue compartments
utilized in the PBPK/PD model different from those of Gearhart et al. (1990)
are listed below:
Oral absorption (gavage). The absorption of CPF following oral adminis-
tration in corn oil vehicle was modeled utilizing a two-compartment model.
The rate of change and amount of CPF in the compartments is described as
dCmpt1
dt
5 2KaS p Cmpt1 2 KsI p Cmpt1
Cmpt1 5E

t
dCmpt1dt.
dCmpt2
dt
5 KsI p Cmpt1 2 KaI p Cmpt2
Cmpt2 5E

t
dCmpt2dt,
dOral
dt
5 KaS p Cmpt1 1 KaI p Cmpt2
where KaS and KaI are the 1st-order rate constant (hr–1) for absorption from
the 1st and 2nd compartments (Cmpts 1 and 2) into the liver compartment, and
KsI (h–1) is the transfer rate constant between GI tract compartments. The rate
of oral absorption (dOraldt) is the sum of the absorption rates from Cmpt1 and
Cmpt2.
Oral absorption (dietary). To model dietary administration of CPF, the
dietary update was modeled as a zero-order process, and was based on the
equations used to describe uptake from drinking water (Andersen et al., 1987
and Corley et al., 1994) as
kzero 5
Diet p Fa
12 hr
,
where Diet is the dietary dose of CPF (mg/kg/day), and Fa is the fractional
absorption (%) of CPF from the diet. The kzero was the zero-order uptake rate
(mmol/h) of CPF from the diet. To model repeated dosing, a 24-h pulsing
routine was incorporated into the model in which food containing CPF was
consumed for a 12-h period over each 24-h interval. The amount of CPF
absorbed from either the gavage or dietary administration was added directly
into the liver compartment.

Dermal absorption. The rate of change in the amount of CPF absorbed
through the skin (ASK, mmol) was described based on previous dermal uptake
PBPK models (Corley et al., 1994; McDougal et al., 1986) as
dADL
dt

Kp p SA

pSConcL 2
ADL
VliqD,
ADL 5E

t
dADLdt,
dASK
dt
5 QSK p ~Caf 2 CVskf! 1
dADL
dt
,
ASK 5E

t
dASKdt,
where, dADLdt is the rate of change of CPF in the skin, Kp is the permeability
constant for CPF (cm/h), SA is the surface area exposed (cm2), ConcL is the
concentration of CPF in liquid (mmol/l), ADL is the amount of CPF in the skin
(mmol), and Vliq is the initial volume of liquid applied to skin (L), QSK is the
blood ﬂow to the skin (L/h), CAf is the free concentration of CPF in arterial
blood (mmol/l), and CVskf is the concentration of free CPF in venous blood
draining the skin (mmol/l).
Liver compartment. The rate of change in the amount of CPF in the liver
(AH, mmol) is described as the rate of free CPF entering the liver as absorbed
dose from the GI tract, or through the systemic circulation minus the rate of
free CPF leaving the liver unchanged, or by metabolism to either CPF-oxon or
TCP as
dAH
dt
5 QH p ~CAHf 2 CVHf! 1
dOral
dt

dt

dAML2
dt
dt

Vmax1 p CH
Km1 1 CH
dAML2
dt

Vmax2 p CH
Km2 1 CH
AH 5E

---CHUNK_BREAK---

p CH Km1 1 CH dAML2 dt Vmax2 p CH Km2 1 CH AH 5E t
dAHdt
CH 5
AH
VH
where QH is the blood ﬂow (l/h) to the liver, CAHf and CVHf are the
concentrations (mmol/l) of free CPF in arterial blood entering the liver and
CPF in venous blood draining the liver, respectively. dOraldt is the rate of
uptake (mmol/h) into the liver compartment from the GI tract, AML1 and
AML2 are the amounts (mmol) of free CPF metabolized to CPF-oxon and TCP
by hepatic CYP450, respectively. Vmax1 and Km1 are the maximum velocity
(mmol/h) and the Michaelis constant (mmol/l) for metabolism to CPF-oxon,
respectively, and Vmax2 and Km2 are the maximum velocity (mmol/h) and the
Michaelis constant (mmol/l) for metabolism to TCP, respectively.
Protein binding of CPF and CPF-oxon. The protein binding of CPF (FBc)
and CPF-oxon (Fbo) were set at a constant fraction (%). Only free (i.e.,
nonbound fraction) CPF, or CPF-oxon were allowed to partition into and out
of each tissue compartment and be available for metabolism (i.e., CYP450,
B-EST, A-EST). The concentration of bound CPF or CPF-oxon in both arterial
and venous blood was continuously calculated as a function of the free CPF or
CPF-oxon in arterial blood or in venous blood draining each tissue compart-
ment to maintain mass balance; the protein binding in plasma was calculated
by the equations
CV 5O
~Qi p CVif!
QC

~Qi p CVib!
QC
,
dABl
dt
5 QC p ~CV 2 CA!,
ABl 5E

t
dABldt,
CA 5
ABl
VBl ,
CAf 5 CA p ~1 2 FB!,
CAb 5 CA p FB,
where CV is the pooled venous blood which is the sum of the free and bound
CPF or CPF-oxon concentrations (mmol/l) in the venous blood draining all the
compartments, Qi is the blood ﬂow to each tissue compartment (l/h), Cvif and
Cvib are the concentrations of free and bound CPF or CPF-oxon, respectively,
in the venous blood draining each compartment, and QC is the cardiac output
(l/h). The total amount of CPF or CPF-oxon and their concentrations in the
blood compartment are ABl (mmol), and CA (mmol/l), and CAf, and CAb are
the concentration of free and bound CPF or CPF-oxon, respectively, in the
arterial blood.
Liver compartment CPF-oxon model. The liver compartment represents the
linkage between the models for CPF and CPF-oxon (See Fig. 1). The rate of
change in the amount of CPF-oxon in the liver (AHo, mmol) is deﬁned as the
rate of input from the metabolism of CPF to CPF-oxon (dAML1dt), plus the
input from the hepatic artery, minus the rate of loss into the venous blood
draining the liver (CVHof), where the blood concentrations available for
partitioning of CPF-oxon into and out of the liver are not bound to protein (i.e.,
free). Additional loss of free CPF-oxon is associated with hepatic A-EST and
B-EST metabolism. according to the equations
dAHo
dt
5 QH p ~CAHof 2 CVHof! 1
dt

dAML3
dt
2S
dAML4
dt

dAML5
dt

dAML6
dt D,
dAML3
dt

Vmax3 p CHo
Km3 1 CHo ,
dAML~4 2 6!
dt
5 AHce p Ki p CHo,
AHo 5E

t
dAHodt,
CHo 5
AHo
VH ,
where the rate of A-EST metabolism (dAML3dt) of CPF-oxon to TCP is
described by Michaelis-Menten kinetics, Vmax3, and Km3 are the maximum
velocity (mmol/h) and Michaelis constant (mmol/l), and the rate (mmol/h) of
hepatic B-EST (i.e., AChE, BuChE, and CaE) metabolism of CPF-oxon to
TCP calculated as the product of the amount of available enzymes (AHce,
mmol), bimolecular inhibition rate constant (Ki, mM/h), and the concentration
of CPF-oxon (CHo, mmol/l) in the liver compartment. Similar equations for
B-EST metabolism of CPF-oxon to TCP were included in the blood, dia-
phragm, and brain compartments; in addition, A-EST metabolism of CPF-oxon
to CPF was also incorporated into the blood compartment.

Tissue concentrations of CPF or CPF-oxon. The rate of change of CPF or
CPF-oxon in tissues that neither form nor eliminate CPF-oxon is similar to that
of Corley et al. (1994), as
dAi
dt 5 Qi p ~CAif 2 CVif!,
where Ai is the amount of CPF or CPF-oxon in the i tissue (mmol/l), and CAif
and CVif are the free concentrations (mmol/l) in the arterial and venous blood
entering and draining, respectively.
B-EST tissue inhibition by CPF-oxon. The equations describing the tissue
(i.e., blood, brain, diaphragm, and liver) inhibition of AChE, BuChE, and CaE
by CPF-oxon are similar to those used to describe B-EST inhibition by DFP
(Gearhart, et al., 1990). For example, the equations describing ChE inhibition
in the liver compartments are
dAHce
dt
5 Ks 2 AHce p ~Kd 1 Ki p CHo! 1 INactive p Kr,
AHce 5E
Ince
t
dAHcedt,
dINactive
dt
5 AHce p Ki p CHo 2 INactive p ~Ka 1 Kr!,
INactive 5E

t
dINactivedt,
where dAHcedt is the rate of change (mmol/h) of tissue ChE enzyme, Ks is the
zero-order enzyme synthesis rate (mmol/h), AHce is the amount (mmol) of
available enzyme, Kd, Kr, and Ka are the 1st-order rates (hr–1) for enzyme
degradation, regeneration, and aging, respectively; Ki (mM/h) is the bimolec-
ular rate of inhibition, INactive is the amount (mmol) of ChE that is inactivated
due to phosphorylation of ChE. These equations were incorporated in all the
model compartments (i.e., liver, brain, diaphragm, and blood) that contained
B-EST activity.
One-compartment model TCP elimination. The pharmacokinetics of TCP in
blood and urine were modeled utilizing a simple one-compartment analysis to
describe blood and urinary elimination, where
dATCP
dt
5SO
dATCP~i!
dt D 2 ~ATCP p Ke!,
ATCP 5E

t
dATCPdt,
dTCPexc
dt
5 ATCP p Ke
TCPexc 5E

---CHUNK_BREAK---

~ATCP p Ke!, ATCP 5E t dATCPdt, dTCPexc dt 5 ATCP p Ke TCPexc 5E t
dTCPexcdt,
cbTCP 5
ATCP
Vd
,
dATCPdt is the rate of change for TCP (mmol/h), in which dATCP(i)dt is the
rate of TCP formation from all sources (i.e., CYP450, A-EST, B-EST), ATCP
is the amount of TCP (mmol), Ke is the 1st order (hr–1) elimination rate
constant, cbTCP is the blood concentration of TCP (mmol/h), and Vd is the
volume of distribution (liter).
ACKNOWLEDGMENTS
We thank Dr. Richard A. Corley for his insightful discussion and advice in
developing this PBPK/PD model and Drs. James C. Kisicki, Cindy Wilinson-
Seip, and Michael L Comb from MDS Harris (Lincoln, NE) for conducting the
human pharmacokinetic/pharmacodynamic studies. This work was supported
through a contract with Dow AgroSciences, Indianapolis IN.
REFERENCES
Abbas, R., and Hayton, W. L. (1997). A physiologically based pharmacoki-
netic and pharmacodynamic model for paraoxon in rainbow trout. Toxicol.
Appl. Pharmacol. 145, 192–201.
Amitai, G., Moorad, D., Adani, R., and Doctor, B. P. (1998). Inhibition of
acetylcholinesterase and butyrylcholinesterase by chlorpyrifos-oxon. Bio-
chem. Pharmacol. 56, 293–299.
Andersen, M. E. (1995). Development of physiologically based pharmacoki-
netic and physiologically based pharmacodynamic models for applications
in toxicology and risk assessment. Toxicol. Lett. 79, 35–44.
Andersen, M. E., Clewell, H. J., III, Gargas, M. L, Smith, F. A., and Reitz,
R. H. (1987). Physiologically based pharmacokinetics and the risk assess-
ment process for methylene chloride. Toxicol. Appl. Pharmacol. 87, 185–
205.
Aprea, C., Sciarra, G., Sartorelli, P., Desideri, E., Amati, R., and Sartorelli, E.
(1994). Biological monitoring of exposure to organophosphorus insecticides
by assay of urinary alkylphosphates: Inﬂuence of protective measures during
manual operations with treated plants. Int. Arch. Occup. Environ. Health 66,
333–338.
Bakke, J. E., Feil, V. J., and Price, C. E. (1976). Rat urinary metabolites from
O,O-diethyl-O-(3,5,6-trichloro-2-pyridyl)phosphorothioate. J. Environ. Sci.
Health Bull. 11, 225–230.
Brown, R. P., Delp, M. D., Lindstedt, S. L., Rhomberg, L. R., and Beliles, R. P.
(1997). Physiological parameter values for physiologically based pharma-
cokinetic models. Toxicol. Ind. Health 13, 407–484.
Brzak, K. A., Harms, D. W., Bartels, M. J., and Nolan, R. J. (1998). Deter-
mination of chlorpyrifos, chlorpyrifos oxon, and 3,5,6-trichloro-2-pyridinol
in rat and human blood. J. Anal. Toxicol. 22, 203–210.
Butler, A. M., and Murray, M. (1997). Biotransformation of parathion in
human liver: Participation of CYP3A4 and its inactivation during microso-
mal parathion oxidation. J. Pharmacol. Exp. Ther. 280, 966–973.
Calabrese, E. J. (1991). Comparative metabolism: The principal causes of
differential susceptibility to toxic and carcinogenic agents. In Principles of
Animal Extrapolation (E. J. Calabrese, Ed.), pp. 203–276. Lewis Publishers,
Chelsea, MI.
Carr, R. L., and Chambers, J. E. (1996). Kinetic analysis of the in vitro
inhibition, aging and reactivation of brain acetylcholinesterase from rat and
channel catﬁsh by paraoxon and chlorpyrifos-oxon. Toxicol. Appl. Pharma-
col. 139, 365–373.
Chambers, J. E., and Chambers, J. W. (1989). Oxidative desulfuration of
chlorpyrifos, chlorpyrifos-methyl, and leptophos by rat brain and liver.
J. Biochem. Toxicol. 4, 201–203.
Chan, L., Balabaskaran, S., Delilkan, A. E., and Ong, L. H. (1994). Blood
cholinesterase levels in a group of Malaysian blood donors. Malays.
J. Pathol. 16, 161–164.
Chanda, S. M., Mortensen, S. R., Moser, V. C. and Padilla, S. (1997).
Tissue-speciﬁc effects of chlorpyrifos on carboxylesterase and cholinester-
ase activity in adult rats: An in vitro and in vivo comparison. Fundam. Appl.
Toxicol. 38, 148–157.
Clement, J. G. (1984). Role of aliesterase in organophosphate poisoning.
Fundam. Appl. Toxicol. 4, S96–105.
Corley, R. A., Bormett, G. A., and Ghanayem, B. I. (1994). Physiologically

---CHUNK_BREAK---

Toxicol. 4, S96–105. Corley, R. A., Bormett, G. A., and Ghanayem, B. I. (1994). Physiologically based pharmacokinetics of 2–butoxyethanol and its major metabolite, 2-bu-
toxyacetic acid, in rats and humans. Toxicol. Appl. Pharmacol. 129, 61–79.
Drevenkar, V., Vasilic, Z., Stengl, B., Frobe, Z., and Rumenjak, V. (1993).
Chlorpyrifos metabolites in serum and urine of poisoned persons. Chem.
Biol. Interact. 87, 315–322.
Ecobichon, D. J., and Comeau, A. M. (1973). Pseudocholinesterases of mam-
malian plasma: Physiocochemical properties and organophosphate inhibi-
tion in eleven species. Toxicol. Appl. Pharmacol. 24, 92–100.
Ellenhorn, M. J., and Barceloux, D. G. (1988). Medical toxicology—Diagnosis
and Treatment of Human poisoning. Elsevier, New York.
Ellman, G. L., Courtney, K. D., Anders, V., Jr., and Geatherstone, R. M.
(1961). A new and rapid colorimetric determination of acetylcholinesterase
activity. Biochem. Pharmacol. 7, 88–95.
Fabrizi, L., Gemma, S., Testai, E., and Vittozzi, L. (1999). Identiﬁcation of the
cytochrome P450 isoenzymes involved in the metabolism of diazinon in the
rat liver. J. Biochem. Mol. Toxicol. 13, 53–61.
Gaines, T. B. (1969). Acute toxicity of pesticides. Toxicol. Appl. Pharmacol.
14, 515–534.
Gearhart, J. M., Jepson, G. W., Clewell, H. J., III, Andersen, M. E., and
Conolly, R. B. (1990). Physiologically based pharmacokinetic and pharma-
codynamic model for the inhibition of acetylcholinesterase by diisopropy-
lﬂuorophosphate. Toxicol. Appl. Pharmacol. 106, 295–310.
Gibson, J. E., Chen, W. L., and Peterson, R. K. D. (1999). How to determine
if an additional 103 safety factor is needed for chemicals: A case study with
chlorpyrifos. Toxicol. Sci. 48, 117–122.
Grifﬁn, P., Mason, H., Heywood, K., and Cocker, J. (1999). Oral and dermal
absorption of chlorpyrifos: A human volunteer study. Occup. Environ. Med.
56, 10–13.
Guengerich, F. P. (1977). Separation and puriﬁcation of multiple forms of
microsomal cytochrome P-450. Activities of different forms of cytochrome
P-450 towards several compounds of environmental interest. J. Biol. Chem.
252, 3970–3979.
Hall, S. D., Thummel, K. E., Watkins, P. B., Lown, K. S., Benet, L. Z., Paine,
M. F., Mayo, R. R., Turgeon, D. K., Bailey, D. G., Fontana, R. J., and
Wrighton, S. A. (1999). Molecular and physical mechanisms of ﬁrst-pass
extraction. Drug Metab. Dispos. 27, 161–166.
Hill, R. H., Head, S. L., Baker, S., Gregg, M., Shealy, D. B., Bailey, S. L.,
Williams, C. C., Sampson, E. J., and Needham, L. L. (1995). Pesticide
residues in urine of adults living in the United States: Reference range
concentrations. Environ. Res. 71, 99–108.
Jochemsen, R., Bazot, D., Brillanceau, M. H., and Lupart, M. (1993). Assess-
ment of drug exposure in rat dietary studies. Xenobiotica 23, 1145–1154.
Kararli, T. T. (1995). Comparison of the gastrointestinal anatomy, physiology,
and biochemistry of humans and commonly used laboratory animals. Bio-
pharm. Drug Dispos. 16, 351–380.
Lanning, C. L., Fine, R. L., Sachs, C. W., Rao, U. S., Corcoran, J. J., and
Abou-Donia, M. B. (1996). Chlorpyrifos oxon interacts with the mammalian
multidrug-resistance protein, P-glycoprotein. J. Toxicol. Environ. Health 47,
395–407.
Loewenherz, C., Fenske, R. A., Simcox, N. J., Bellamy, G., and Kalman, D.
(1997). Biological monitoring of organophosphorus pesticide exposure
among children of agricultural workers in central Washington state. Envi-
ron. Health Perspect. 105, 1344–1353.
Lotti, M., Moretto, A., Zoppellari, R., Dainese, R., Rizzuto, N., and Barusco,
G. (1986). Inhibition of lymphocytic neuropathy target esterase predicts the
development of organophosphate-induced delayed polyneuropathy. Arch.
Toxicol. 59, 176–179.
Ma, T., and Chambers, J. E. (1994). Kinetic parameters of desulfuration and
dearylation of parathion and chlorpyrifos by rat liver microsomes. Food
Chem. Toxicol. 32, 763–767.
Ma, T., and Chambers, J. E. (1995). A kinetic analysis of hepatic microsomal
activation of parathion and chlorpyrifos in control and phenobarbital-treated
rats. J. Biochem. Toxicol. 10, 63–68.
Maxwell, D. M., Lenz, D. E., Groff, W. A., Kaminskis, A., and Froehlich,
H. L. (1987). The effect of blood ﬂow and detoxiﬁcation on in vivo
cholinesterase inhibition by soman in rats. Toxicol. Appl. Pharmacol. 88,
66–76.
Maxwell, D. M., Vlahacos, C. P., and Lenz, D. E. (1988). A pharmacodynamic
model for soman in the rats. Toxicol. Lett. 43, 175–188.
McCollister, S. B., Kociba, R. J., Humiston, C. G., and McCollister, D. D.
(1974). Studies on the acute and long-term oral toxicity of chlorpyrifos
(o,o-diethyl-o-(3,5,6-trichloro-2-pyridyl) phosphorothioate). Food Cosmet.
Toxicol. 12, 45–61.
McDougal, J. N., Jepson, G. W., Clewell, H. J., III, MacNaughton, M. G., and
Andersen, M. E. (1986). A physiological pharmacokinetic model for dermal
absorption of vapors in the rat. Toxicol. Appl. Pharmacol. 85, 286–294.
Mortensen, S. R., Brimijoin, S., Hooper, M. J., and Padilla, S. (1998). Com-
parison of the in vitro sensitivity of rat acetylcholinesterase to chlorpyrifos-
oxon: What do tissue IC50 values represent? Toxicol. Appl. Pharmacol. 148,
46–49.
Mortensen, S. R., Chanda, S. M., Hooper, M. J., and Padilla, S. (1996).
Maturational differences in chlorpyrifos-oxonase activity may contribute to
age-related sensitivity to chlorpyrifos. J. Biochem. Toxicol. 11, 279–287.
Murphy, S. D. (1986). Toxic effects of pesticides. In Casarett and Doull’s
Toxicology, The Basic Science of Poison, 3rd ed. (C. D. Klaassen, M. O.
Amdur, and J. Doull, Eds.), pp. 519–581. MacMillam, New York.
Neal, R. A. (1980). Microsomal metabolism of thiono-sulfur compounds,
mechanisms, and toxicological signiﬁcance. In Reviews in Biochemical
Toxicology (E. Hodgson, J. R. Bend, and R. M. Philpot, Eds.) Vol. 2, pp.
131–172. Elsevier-North Holland, New York.
Nolan, R. J., Rick, D. L., Freshour, N. L., and Saunders, J. H. (1984).
Chlorpyrifos: Pharmacokinetics in human volunteers. Toxicol. Appl. Phar-
macol. 73, 8–15.
Nostrandt, A. C., Padilla, S., and Moser, V. C. (1997). The relationship of oral
chlorpyrifos: Effects on behavior, cholinesterase inhibition, and muscarinic-
receptor density in rat. Pharmacol. Biochem. Behav. 58, 15–23.
Obach, R. S., Zhang, Q.-Y., Dunbar, D., and Kaminsky, L. S. (2001). Meta-
bolic characterization of the major human small intestinal cytochrome
P450s. Drug Metab. Dispos. 29, 347–352.
ORNL (2000). Appendix G: Inhibition of cholinesterases and an evaluation of
the methods used to measure cholinesterase activity. Oak Ridge National
Laboratory. J. Toxicol. Environ. Health A 59, 519–526.
Paine, M. F., Schmiedlin-Ren, P., and Watkins, P. B. (1999). Cytochrome
P-450 1A1 expression in human small bowel: Interindividual variation and
inhibition by ketoconazole. Drug Metab. Dispos. 27, 360–364.
Poet, T. S. (2000). Assessing dermal absorption. Toxicol. Sci. 58, 1–2.
Poet, T. S., Corley, R. A., Thrall, K. D., Edwards, J. A., Tanojo, H., Weitz,
K. K., Hui, X., Maibach, H. I., and Wester, R. C. (2000). Assessment of the
percutaneous absorption of trichloroethylene in rats and humans using
MS/MS real-time breath analysis and physiologically based pharmacoki-
netic modeling. Toxicol. Sci. 56, 61–72.
Pond, A. L., Chambers, H. W., and Chambers, J. E. (1995). Organophosphate
detoxiﬁcation potential of various rat tissues via A-esterase and aliesterase
activity. Toxicol. Lett. 78, 245–252.
Poulin, P., and Krishnan, K. (1995). An algorithm for predicting tissue: blood
partition coefﬁcients of organic chemicals from n-octonol: Water partition
coefﬁcient data. J. Toxicol. Environ. Health 46, 117–129.
Quackenboss, J. J., Pellizari, E., Freeman, N., Head, S., Whitmore, R., Zelan,
H., and Stroebel, C. (1998). Use of Screening Questionnaires to Identify
Exposed and Sensitive Population Groups in the Region V NHEXAS Chil-
dren’s Pesticide Study. Presented at the Tenth Conference of the Interna-

---CHUNK_BREAK---

Region V NHEXAS Chil- dren’s Pesticide Study. Presented at the Tenth Conference of the Interna- tional Society of Environmental Epidemiology and Eighth Conference of the
International Society of Exposure Analysis, Boston.
Ramsey, J. C., and Andersen, M. E. (1984). A physiologically based descrip-
tion of the inhalation pharmacokinetics of styrene in rats and humans.
Toxicol. Appl. Pharmacol. 73, 159–175.
Renwick, A. G. (1994). Toxicokinetics-pharmacokinetics in toxicology. In
Principles and Methods of Toxicology, 3rd ed. (A. W. Hayes, Ed.), pp. 101
–147. Raven Press, New York.
Richter, E. D., Kowalski, M., Leventhal, A., Grauer, F., Marzouk, J., Brenner,
S., Shkolnik, I., Lerman, S., Zahavi, H., Bashari, A., Peretz, A., Kaplanski,
H., Gruener, N., and Ben Ishai, P. (1992). Illness and excretion of organo-
phosphate metabolites four months after household pest extermination.
Arch. Environ. Health 47, 135–138.
Sams, C., Mason, H. J., and Rawbone, R. (2000). Evidence for the activation
of organophosphate pesticides by cytochromes P450 3A4 and 2D6 in human
liver microsomes. Toxicol. Lett. 116, 217–221.
Schalm, O. W., Ed. (1961). Veterinary hematology. Lea and Febiger, Phila-
delphia, PA.
Schmiedlin-Ren, P., Benedict, P. E., Dobbins, W. O., III, Ghosh, M., Kolars,
J. C., and Watkins, P. B. (1993). Cultured adult rat jejunal explants as a
model for studying regulation of CYP3A. Biochem. Pharmacol. 46, 905–
918.
Shurdut, B. A., Barraj, L., and Francis, M. (1998). Aggregate exposures under
the Food Quality Protection Act: An approach using chlorpyrifos. Regul.
Toxicol. Pharmacol. 28, 165–177.
Staats, D. A., Fisher, J. W., and Conolly, R. B. (1991). Gastrointestinal
absorption of xenobiotics in physiologically based pharmacokinetic models.
A two-compartment description. Drug Metab. Disp. 19, 144–148.
Sultatos, L. G. (1990). A physiologically based pharmacokinetic model of
parathion based on chemical-speciﬁc parameters determined in vitro.
J. Amer. Coll. Toxicol. 9, 611–619.
Sultatos, L. G. (1994). Mammalian toxicology of organophosphorus pesti-
cides. J. Toxicol. Environ. Health 43, 271–289.
Sultatos, L. G., and Murphy, S. D. (1983). Kinetic analyses of the microsomal
biotransformation of the phosphorothioate insecticides chlorpyrifos and
parathion. Fundam. Appl. Toxicol. 3, 16–21.
Sultatos, L. G., Shao, M., and Murphy, S. D. (1984). The role of hepatic
biotransformation in mediating the acute toxicity of the phosphorothionate
insecticide chlorpyrifos. Toxicol. Appl. Pharmacol. 73, 60–68.
U. S. EPA (1998). Health effects of pesticides. In The EPA Children’s
Environmental Health Yearbook, U. S. Environmental Protection Agency,
Ofﬁce of Children’s Health Protection.
Vale, J. A. (1998). Toxicokinetic and toxicodynamic aspects of organophos-
phate (OP) insecticide poisoning. Toxicol. Lett. 102–103, 649–652.
Vasilic, Z., Drevenkar, V., Rumenjak, V., Stengl, B., and Frobe, Z. (1992).
Urinary excretion of diethylphosphorus metabolites in persons poisoned by
quinalphos or chlorpyrifos. Arch. Environ. Contam. Toxicol. 22, 351–357.
Venkataraman, B. V., and Rani, M. A. (1994). Species variation in the
speciﬁcity of cholinesterases in human and rat blood samples. Indian
J. Physiol. Pharmacol. 38, 211–213.
Watkins, P. B. (1992). Drug metabolism by cytochromes P450 in the liver and
small bowel. Gastroenterol. Clin. North Am. 21, 511–526.
Wester, R. C., Maibach, H. I., Bucks, D. A. W., and Guy, R. H. (1983).
Malathion percutaneous absorption after repeated administration to man.
Toxicol. Appl. Pharmacol. 68, 116–119.
Wester, R. C., Maibach, H. I., Melendres, J., Sedik, L., Knaak, J., and Wang,
R (1992). In vivo and in vitro percutaneous absorption and skin evaporation
of isofenphos in man. Fundam. Appl. Pharmacol. 19, 521–526.
Wester, R. C., Sedik, L., Melendres, J., Logan, F., Maibach, H. I., and Russell,
I. (1993). Percutaneous absorption of diazinon in humans. Food Chem.
Toxicol. 31, 569–572.
Withey, J. R., Collins, B. T., and Collins, P. G. (1983). Effect of vehicle on the
pharmacokinetics and uptake of four halogenated hydrocarbons from the
gastrointestinal tract of the rat. J. Appl. Toxicol. 3, 249–253.
Yano, B. L., Young, J. T., and Mattsson, J. L. (2000) Lack of carcinogenicity
of chlorpyrifos insecticide in a high-dose, 2-year dietary toxicity study in
Fischer 344 rats. Toxicol. Sci. 53, 135–144.
Zhang, Q.-Y., Dunbar, D., Ostrowska, A., Zeisloft, S., Yang, J., and Kaminsky,
L. S. (1999). Characterization of human small intestinal cytochromes P-450.
Drug Metab. Dispos. 27, 804–809.
Zheng, Q., Olivier, K., Won, Y. K., and Pope, C. N. (2000). Comparative
cholinergic neurotoxicity of chlorpyrifos exposures in pre-weanling and
adult rats. Toxicol. Sci. 55, 124–132.