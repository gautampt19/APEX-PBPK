TOXICOKINETICS AND METABOLISM
https://doi.org/10.1007/s00204-025-04261-3
Abbreviations
PCB	
Polychlorinated biphenyl
PBPK	
Physiologically based pharmacokinetic
RfD	
Reference dose
POP	
Persistent organic pollutants
T1/2	
Half-life
ADME	
Absorption: distribution: metabolism: and 
excretion
AUCinf 
Area under the curve to infinity

 Seung-Hyun Jeong
jeongsh@scnu.ac.kr

College of Pharmacy, Chonnam National University, 77 
Yongbong-Ro, Buk-Gu, Gwangju 61186, Republic of Korea

College of Pharmacy, Sunchon National University, 255 
Jungang-Ro, Suncheon-Si, Jeollanam-Do 
57922, Republic of Korea

College of Pharmacy and Research Institute of Life and 
Pharmaceutical Sciences, Sunchon National University, 
Suncheon-Si 57922, Republic of Korea
Abstract
Polychlorinated biphenyl-153 (PCB-153) is a representative organic pollutant that can accumulate in the human body, 
particularly in adipose tissue, for long periods due to its environmental persistence and high lipid solubility. Existing risk 
assessments primarily rely on simple extrapolations based on blood concentrations, and a quantitative approach that con­
siders internal exposure at the tissue level is lacking. The main objective of this study was to establish a human physiologi­
cally based pharmacokinetic (PBPK) model for PCB-153 and to quantitatively predict tissue accumulation in the human 
body based on this model, thereby suggesting the possibility of expanding its application as a precise and scientific human 
risk assessment tool in the future. Based on existing mouse experimental data, a PBPK model was constructed and vali­
dated, and a whole-body human PBPK model was established through interspecies extrapolation. Monte Carlo simulations 
were then performed, considering physiological variations in the adult population, to predict concentration–time curves 
for major human tissues (fat, liver, brain, skin, and plasma) following a single dose (20 mg/kg) and repeated exposures at 
the reference dose (RfD) level (5.86 ng/kg/day). The simulation results based on the human PBPK model established in 
this study showed that adipose tissue showed the highest accumulation pattern with an average partition coefficient (Kp) 
of 795,725 after a single dose (20 mg/kg), and even under repeated exposure conditions (RfD), the average Kp in adipose 
tissue was found to be 4961, the highest among all tissues. In addition to adipose tissue, PCB-153 was widely distributed 
in the brain, skin, liver, etc., and the same pattern was observed in terms of steady-state concentrations upon repeated 
administration. These results strongly suggest the possibility of PCB-153 accumulation in major organ tissues even at 
relatively low external exposure doses (RfD), and support the need for a conservative and quantitative risk assessment, 
especially for the possibility of chronic toxicity due to long-term exposure. The human PBPK model established in this 
study establishes a foundation for numerically quantifying the tissue-specific accumulation characteristics of PCB-153, 
suggesting an alternative approach that overcomes the limitations of existing, limited risk assessments. This model can 
serve as a scientific basis for future human exposure assessments and standardization of highly soluble environmental 
pollutants.
Keywords  Polychlorinated biphenyl-153 · Tissue distribution · Physiologically based pharmacokinetic model · 
Interspecific extrapolation · Reference dose · Risk assessment
Received: 24 September 2025 / Accepted: 20 November 2025 / Published online: 26 December 2025
© The Author(s), under exclusive licence to Springer-Verlag GmbH Germany, part of Springer Nature 2025
Physiologically based pharmacokinetic modeling of polychlorinated 
biphenyl-153: cross-species extrapolation and human exposure 
simulation
Ji-Hun Jang1 · Seung-Hyun Jeong2,3
1 3

---CHUNK_BREAK---

polychlorinated biphenyl-153: cross-species extrapolation and human exposure simulation Ji-Hun Jang1 · Seung-Hyun Jeong2,3 1 3 Clast	
Concentration at the last time point
Cmax	
Maximum concentration
Tmax	
Time to reach Cmax
MRT	
Mean residence time
Vd	
Volume of distribution
Ctrough	
Minimum concentration at steady state
VPC	
Visual predictive check
Introduction
Polychlorinated biphenyls (PCBs) were widely used 
for industrial purposes until the mid-twentieth century, 
and have since been considered representative persis­
tent organic pollutants (POPs) due to their high stabil­
ity and persistence in the environment (Jones and de 
Voogt 1999; Sandu et al. 2025). Among these, PCB-153 
(2,2',4,4',5,5'-hexachlorobiphenyl) is one of the isomers 
with the highest residual levels in the environment and 
in living organisms, and various biological toxic effects 
have been reported (Grilo et al. 2014; Safe 1994). In par­
ticular, because it has a strong lipophilicity and a very 
long biological half-life (T1/2) exceeding several years, 
it is highly likely to accumulate in the body, raising con­
cerns about long-term health effects after exposure (Rit­
ter et al. 2011; Weijs et al. 2010). PCB-153 has been 
repeatedly detected in serum and adipose tissue in the 
general population, and according to the US NHANES 
survey, the average blood PCB-153 concentration was 
found to be 14.5‒19.8 ng/g lipid (Crinnion 2010). Even 
in the WHO/UNEP Global Survey, serum concentrations 
of PCB-153 varied widely, ranging from 10 to 83 ng/g 
lipid in Europe and North America (McLachlan et al. 
2018; Undeman et al. 2018). In South Korea, accord­
ing to the 5th Environmental Health Basic Survey, the 
average blood exposure level of PCB-153 for adults was 
7.15 ng/g lipid (ME 2024).
PCB-153 can indirectly inhibit or activate the cytochrome 
P450 system, a liver metabolic enzyme, and these actions 
are associated with hepatotoxicity, endocrine disruption, 
developmental toxicity, and reproductive toxicity (Ferrante 
et al. 2014; Lindell 2012). It has also been reported that it 
can induce intracellular oxidative stress and inhibit mito­
chondrial function, thereby inducing mechanisms related to 
apoptosis or carcinogenesis (Glauert et al. 2008). Recently, 
animal experiments have shown that PCB-153 can reach the 
brain and nervous system, and can also cause neurotoxicity 
and neurobehavioral changes (Klocke and Lein 2020; Seel­
bach et al. 2010). Despite the elucidation of various toxicity 
mechanisms, quantitative prediction and interpretation tools 
for the tissue distribution and in vivo behavior of PCB-153 
are extremely limited.
Previous studies on PCB-153 have been limited to envi­
ronmental concentration monitoring, biological sample 
analysis, epidemiological correlation analysis, or in vitro 
and in vivo toxicity assessments. Model-based approaches 
that can quantitatively explain or predict systemic tissue dis­
tribution and exposure levels have been virtually nonexis­
tent. In particular, a physiologically based pharmacokinetic 
(PBPK) model that can provide a quantitative link between 
exposure levels and tissue accumulation has not yet been 
reported for PCB-153. This gap presents a major obstacle to 
reliable human dose prediction from a risk assessment per­
spective. Indeed, numerous toxicology and environmental 
health researchers have raised the urgent need for a preclini­
cal model-based quantitative interpretation system for PCB-
153 (Chain 2015; Organization 2010).
In this study, we newly developed a PBPK model for 
PCB-153. We first established a PBPK model for mice 
and then performed interspecies extrapolation to humans 
based on this. In particular, we calibrated the model 
using existing tissue-specific distribution data for mice, 
and implemented a PBPK model capable of predicting 
tissue-specific exposure in the body, thereby providing a 
scientific basis for future risk assessment of PCB-153. In 
addition, we used this model to estimate the concentra­
tion distribution patterns and PK parameters of PCB-153 
in major tissues such as brain, liver, fat, skin, and plasma 
at the previously reported human reference dose (RfD) 
level (Ermler and Kortenkamp 2022).
The scientific significance of this study can be empha­
sized in three key aspects. First, this study developed the 
first whole-body, tissue-based PBPK model for PCB-153, 
providing a quantitative framework for predicting bioac­
cumulation and tissue-specific concentrations. Second, 
by extrapolating the established mouse model to humans, 
we demonstrated its applicability as a foundational tech­
nology for future quantitative human health risk assess­
ments. Third, to validate the model, we evaluated its PK 
fit and reliability from various perspectives, including 
residual analysis, two-fold error analysis, and sensitiv­
ity analysis. This represents a significant contribution to 
toxicological quantification, distinguishing it from con­
ventional qualitative and technical approaches. In this 
respect, this study is an attempt to provide a scientific 
framework for quantitatively approaching the accumula­
tion and hazard prediction in major human tissues due 
to chronic exposure to PCB-153, and has great academic 
and practical significance in that it develops a precise 
toxicodynamic analysis tool for setting safety standards 
for environmental toxicants and predicting their effects 
on the human body.
1 3

---CHUNK_BREAK---

safety standards for environmental toxicants and predicting their effects on the human body. 1 3 Methods
Collecting modeling requirements data for PCB-153
To build a PBPK model for PCB-153, we first systemati­
cally collected physicochemical and biochemical property 
information that could be used as modeling inputs for the 
compound based on the literature. Because these inputs 
directly impact the structural validity and predictive accu­
racy of the PBPK model, a rigorous information selection 
process utilizing reliable data sources was required. The 
literature search was conducted using major science-based 
databases such as PubMed, ScienceDirect, Google Scholar, 
and ECHA Substance Info, and the search strategy was 
established centered on the following keywords: “PCB-
153,” “Pharmacokinetics,” “ADME (absorption, distribu­
tion, metabolism, and excretion)” “Tissue distribution,” 
“Biochemical parameters,” “Partition coefficient,” “PBPK 
modeling,” “Absorption,” “Metabolism,” “Clearance,” and 
“Lipophilicity.” An initial literature screening of over 150 
papers was conducted. Review papers that did not provide 
direct numerical information (data-based parameter values) 
on the PK behavior or modeling of PCB-153, or tissue-spe­
cific distribution/metabolism information, environmental 
monitoring-focused studies, or papers that only addressed 
congeners were excluded. Furthermore, papers that compre­
hensively addressed “PCBs” were excluded if PCB-153 was 
not explicitly addressed as the primary compound.
To obtain the essential in vivo time-course tissue concen­
tration data for the development and validation of the PBPK 
model, we searched for reports on mouse tissue distribu­
tion experiments on single components of PCB-153 acces­
sible within the literature screening index. Among these, the 
study by Lee et al. (Lee et al. 2002) provided data on the 
changes in concentrations in liver, brain, fat, and skin tissues 
over time following a single oral administration of 20 mg/kg 
of PCB-153 to non-pregnant adult female mice. This study 
was utilized as the most crucial experimental report for the 
model development of this study (which aimed to quantify 
the level of PCB-153 exposure in the general population).
In this report (Lee et al. 2002), the concentrations of 
PCB-153 in each tissue (liver, brain, adipose tissue, skin tis­
sue) were measured at time points 1, 6, and 13 days after 
administration, and at time points 2 and 14  days (liver, 
brain, adipose tissue) using a gas chromatography-based 
analysis method, and the concentration unit was expressed 
as ng/g tissue. The mean value and standard deviation for 
each tissue at each time point were reported together to 
enable quantitative comparison in model fitting and valida­
tion. In this study, these graph data were digitized using the 
WebPlotDigitizer program (version 4.7) to secure a data­
set, which enabled quantitative comparison with the PBPK 
model simulation results. The literature-based physico­
chemical, biochemical, and experimental tissue concentra­
tion datasets obtained in this procedure served as essential 
foundational information for ensuring structural validity 
and evaluating parameter adequacy of the PCB-153 PBPK 
model developed in this study.
Mouse PBPK model development
A PBPK model to quantitatively describe the in vivo tissue 
distribution and PK behavior of PCB-153 was developed 
using PK-Sim® (version 12, Open Systems Pharmacology 
Suite), which is a validated, mechanistic PBPK platform 
widely used in regulatory science and toxicology mod­
eling. PK‑Sim® employs internally defined differential 
mass‑balance equations to govern substance kinetics across 
physiological compartments. The modeling target was non-
pregnant adult female mice, which closely mirrored the con­
ditions used in the experimental validation (Lee et al. 2002).
The PBPK model follows a whole-body-based archi­
tecture, with major tissue compartments including plasma, 
liver, kidney, brain, fat, skin, lung, GI tract, heart, and mus­
cle. Each tissue compartment is interconnected based on 
physiological characteristics such as tissue volume, blood 
flow, fat, and water content, and drug distribution between 
tissues is implemented according to the tissue-to-plasma 
partition coefficient (Kp). This architecture was automati­
cally built based on the “Mouse (female, adult)” physi­
ological parameter library provided in the default species 
template of PK-Sim®, and the default values were main­
tained without additional modification.
Drug-specific input parameters consisted of previously 
collected literature-based physicochemical and biochemi­
cal information. These included molecular weight, Log P 
(n-octanol/water Kp), aqueous solubility, pKa (acid disso­
ciation constant), fraction unbound in plasma, membrane 
permeability, absorption rate constant, dissolution or deg­
radation rate in the gastrointestinal tract, hepatic clearance, 
and tissue-plasma Kp. These values were mostly supple­
mented by literature-based experimental data, predicted 
values based on similar structural compounds, or struc­
ture-based outputs, and were ultimately optimized through 
model calibration based on fitting between observed and 
predicted values.
To reflect oral administration (oral gavage) conditions 
in the model, the “oral administration via gavage” option 
was applied, and the administered dose was set to 20 mg/
kg body weight, the same as the experimental conditions 
(Lee et al. 2002). Absorption occurs through primary diffu­
sion from the intestine, and the distribution of dissolution 
and absorption regions in the small and large intestines was 
automatically determined according to the gastrointestinal 
1 3

---CHUNK_BREAK---

in the small and large intestines was automatically determined according to the gastrointestinal 1 3 model’s key outputs dynamically match literature-based 
experimental results.
During the calibration process, the parameters selected as 
correction targets were judged to have high predictive sensi­
tivity and high literature-based uncertainty within the over­
all model structure. Parameter optimization was performed 
using a multi-compartment simultaneous fitting method for 
multiple target tissues (liver, brain, fat, skin) rather than 
a single-tissue-based fitting method. Model overfitting, 
which compromises the model’s physiological validity by 
maximizing the predictive fit of only a specific tissue, was 
intentionally avoided. To this end, the search range for each 
parameter was initially set to a value based on physiological 
and biochemical values reported in the literature (Tables 1 
and 2) and was adjusted to maintain biological explainability. 
The goodness-of-fit assessment of the model’s calibration 
results was performed using both qualitative visual compar­
isons and quantitative statistical indicators. First, for visual 
evaluation, a visual predictive check (VPC) was performed 
between the model-predicted concentration–time curves for 
each tissue and the observed values from the literature. This 
included model-predicted confidence intervals, prediction 
intervals, and VPC intervals, and a visual assessment was 
physiology model of PK-Sim®. Initial simulations of the 
model were performed through time-concentration pro­
file generation, and the total simulation period was set to 
14 days (336 h) to enable comparison with experimentally 
reported values (Lee et al. 2002). All simulations were per­
formed with a time step of 0.25 h every 15 min, and the 
calculated concentration units could be converted to ng/g 
tissue or µg/L using a concentration unit converter within 
PK-Sim®. After model construction and initial condition 
setting, no link to MoBi® (Open Systems Pharmacology 
Suite) was used, and complete simulations and subsequent 
parameter optimization were configured solely with func­
tions within PK-Sim®.
Model calibration and validation
The developed mouse PBPK model underwent a model 
parameter calibration process to ensure maximum quanti­
tative agreement with experimental data. This process uti­
lized the built-in parameter identification module within 
PK-Sim®, and its primary goal was to optimize the values 
of key model parameters within realistic ranges so that the 
Table 1  Summary of previously reported and known in vivo pharmacokinetic (PK) properties of PCB-153
PK main 
category
Description
Oral Absorption: PCB-153 is highly lipid-soluble (Log P ≈ 7.2), resulting in greater than 95% absorption when 
administered orallya
Absorption rate: Gastric-intestinal absorption constant ≈ 0.08‒0.42 h−1a,b
Main absorption route: Binds to intestinal lipids and is absorbed via the lymphatic system. Binds to blood VLDL 
and is distributed throughout tissues
Characteristics: PCB-153 can be evaluated to be efficiently and rapidly absorbed during gastroduodenal transit 
when administered orally and to be distributed systemically
Main tissue distribution: PCB-153 accumulates in adipose tissue, with over 70% accumulationa
Kp: Fat/blood of approximately 300a
Plasma protein binding: Over 90% bound to albumin, VLDL, etc.a
Also distributed to brain, liver, and skin: Liver (hepatic distribution Kp ≈ 10)a, brain (Kp ≈ 2.5)a
T1/2: In humans, the T1/2 in the fat compartment is 10–20 yearsc
Metabolism
Main metabolic organ: Liver
Metabolic mechanism: Slow hydroxylation by P450 enzymes such as CYP2B, CYP3A, and CYP2E1
Metabolic rate constant: Approximately 0.00016 h−1a,b in humans
Metabolites: Hydroxylated PCBs (e.g., 3-OH-PCB-153), glucuronic conjugates
Characteristics: Very slow metabolism, structurally resistant, leading to long-term accumulation in the body
Excretion
Main excretion route: Bile (liver → intestine → feces) is the primary excretion route, with only small amounts of 
plasma-soluble metabolites excreted via the kidneys (urine)a
Specificity of excretion during lactation: More than 40% of PCB-153 in nursing mothers is transferred to the 
infant through breast milka
Enterohepatic circulation: After excretion via the bile, a portion is reabsorbed in the small and large intestine, 
significantly extending the T1/2
a
Excretion ratio: > 80% bile/feces, < 10% kidneys (urine), < 5% breast milk/sebum, etc.a
VLDL Very low-density lipoprotein, Kp Partition coefficient, T1/2 Half-life
a This is confirmed to be derived based on mouse PK experimental data
b This is confirmed by estimates obtained through modeling
c Rough estimate
1 3

served as an important comparative indicator for ensuring 
the reliability of the PBPK model’s PK predictions. Finally, 
a normality test of residuals (Shapiro–Wilk test) was also 
performed to determine whether the statistical distribution 
of prediction errors conformed to normality. Through this 
procedure, we were able to evaluate from various angles 
whether the model satisfies both physiological/pharmaco­
dynamic validity and mathematical consistency, and model 
optimization through calibration served as a key step in 
developing a model that can quantitatively reproducibly 
describe the time-concentration distribution kinetics in tar­
get tissues.
Sensitivity analysis
In this study, we conducted a sensitivity analysis to quan­
titatively analyze the impact of key model parameters 
on prediction results. This analysis aims to improve the 
made of how well the observed values overlapped within 
these intervals. The generated ranges were based on Monte 
Carlo simulations, which, unlike population protocol-based 
simulations, means that the predicted results reflect only 
the variability of the parameters themselves, rather than the 
physiological diversity between hypothetical populations.
Quantitative validation was conducted from various 
perspectives using various statistical indicators. First, lin­
ear regression analysis was performed on the relationship 
between observed and predicted values to calculate the R2 
value and regression coefficient (slope), and systematic 
overestimation or underestimation of the predicted values 
was identified. Second, residual analysis was performed 
to confirm the stability of prediction errors over time and 
to visually confirm whether residuals tended to be biased 
toward specific time periods. Third, two-fold error range 
analysis was performed to determine the proportion of pre­
dicted values within two times the observed value, which 
Table 2  Summary of input parameters used in the establishment of the initial physiologically based pharmacokinetic (PBPK) model for PCB-153
Category
Parameters
Units
Input 
information
Physicochemical
Molecular weight
g/mol
360.9
Chemical formula
NA
C12H4Cl6
Lipophilicity (Log P; XLogP3a)
NA
7.2
PubChem (2025)
Solubility at pH 7.0 (at pure water)
μg/L
0.91
Ahmad et al. (2019)
pKa
NA
NAb
Hydrogen bond donor count
NA

Hydrogen bond acceptor count
NA

---CHUNK_BREAK---

al. (2019) pKa NA NAb Hydrogen bond donor count NA Hydrogen bond acceptor count NA Binding proteinc
NA
Albumin; 
Lipoproteins
PubChem (2025); Rodriguez et al. 
(2016)
Fraction unbound (Fu)
%
5.0d
PubChem (2025); Rodriguez et al. 
(2016)
Specific intestinal permeability (transcellular)
5.76
Parameter m for correlation of intestinal permeability 
(transcellular)
NA
1.11
Parameter b for correlation of intestinal permeability 
(transcellular)
NA
0.00
Specific intestinal permeability (paracellular)
0.01
Aqueous diffusion coefficient of drug
cm2/min
3.07 × 10–4
Fraction recycled to plasma (from tissues)
NA
1.00
Partition rate (between plasma and blood cells)
173.96
Elimination
Plasma clearance (liver)
1.45 × 10–5
Specific clearance (liver)
1.08 × 10–4
Specific clearance (endosome)
0.21
Plasma clearance (biliary)
1.31 × 10–5
Specific clearance (biliary)
9.74 × 10–5
Formulation
Type
NA
Dissolved
Assumede
NA Not applicable, pKa Acid dissociation constant
a It implied that the values were derived through prediction and simulation via software
b Structure-based deterministic values
c PCB-153 is reported to interact with many proteins in the body, but its primary partners are lipoproteins (~ 15%), followed by albumin (~ 85%)
d Although specific values have not been reported, it was applied based on estimates that it would be over 90% (protein binding) considering 
the characteristics of similar structural materials
e Considering the high solubility and excellent absorption properties in the body, which are common among exposure media of PCB-153
1 3

PCB-153, and it is known that the difference in biochemical 
pathways depending on the species is relatively small (Dahl 
et al. 2010), so the calculation methodology applied in the 
mouse model was applied identically to the human model. 
However, all of these calculation methods mechanistically 
predict tissue partitioning and permeability together with 
the physicochemical properties of the substance (e.g., Log 
P, pKa, molecular weight, etc.) by considering the physio­
chemical components of each tissue within each species, 
especially the lipid content, water content, and protein con­
tent within the tissue. Although the calculation methods are 
the same, the coefficient values that are actually reflected 
are species-specific. Furthermore, physicochemical prop­
erties of PCB-153, such as lipophilicity, fraction unbound, 
pKa, and solubility, are species-independent and inherent 
to the substance. Therefore, these values, optimized for the 
mouse model, were applied to the human model as is. This 
consistent application was a strategy to enhance model com­
parability and minimize the potential for parameter adjust­
ments during interspecies extrapolation. Consequently, the 
human model construction performed in this study followed 
the same compartment framework structurally as the mouse 
model, but adjusted only the physiological and biochemical 
parameters to fit human characteristics, which is consistent 
with the general approach of preclinical-to-clinical predic­
tive modeling (Patel et al. 2025).
Human model simulation and tissue-level exposure 
prediction
Based on the established human PBPK model, a simulation 
was performed to predict the tissue distribution and expo­
sure profile of PCB-153 in humans. The simulation was 
designed to predict the PKs in humans under single-dose 
and repeat-dose conditions based on the RfD identified in 
a recent report (Ermler and Kortenkamp 2022), as well as 
at the same level as the single dose experimentally applied 
in mice. The simulation was performed using the Popula­
tion Simulation module in the PK-Sim® software, which 
was configured to reflect the PK distribution and variabil­
ity at the population level by generating a virtual popula­
tion of 100 individuals with various physiological variables 
(e.g., body weight, hepatic blood flow, plasma protein con­
centration, etc.) based on a given adult population profile 
and performing repeated individual simulations on these 
populations.
To identify sex-specific PK differences in the compo­
sition of the generated population, the same simulations 
were performed in parallel for each of the three groups (a 
1:1 mixed group of males and females, all males, and all 
females). These sex-based population simulations were 
intended to quantitatively assess the potential differences in 
model’s predictive reliability and identify key factors that 
should be prioritized for adjustment during future param­
eter optimization (calibration). The analysis was conducted 
using the “Sensitivity Analyses” module built into PK-Sim® 
and targeted all input parameters constituting the whole-
body PBPK model. In the sensitivity analysis process, each 
parameter was independently varied within a ± 10% range 
relative to the reference value, and the sensitivity of the 
model’s predicted results was assessed accordingly. More 
specifically, the relative impact of each parameter change 
on exposure levels in target tissues (liver, brain, fat, skin, 
and plasma) was quantitatively assessed. To this end, simu­
lations were performed for each tissue, and predicted PK 
parameters such as AUCinf (area under the curve to infinity) 
and Clast (concentration at the last time point) were quantita­
tively extracted. The analysis results were interpreted based 
on the magnitude of the influence of individual parameter 
changes on the predicted tissue-specific concentration–time 
curve, and the relative influence was quantified by calculat­
ing the sensitivity coefficient. The sensitivity coefficient is 
expressed as follows: (ΔY/Y)/(ΔP/P), where Y is the model 
output value and P is the input parameter. This coefficient 
linearizes the sensitivity of the parameter change to the out­
put result, making it interpretable. A larger value indicates a 
greater influence of the parameter on the model prediction. 
The model sensitivity analysis process allowed us to iden­
tify which drug-specific parameters had the greatest impact 
on PCB-153 accumulation or clearance in specific tissues, 
and this information was useful for rationally selecting 
parameters to prioritize during subsequent model calibra­
tion and extrapolation to human models.
Interspecies extrapolation to human PBPK model
In this study, we performed interspecies extrapolation of 
a PBPK model of PCB-153, developed and optimized in 
mice, to adult female humans. This extrapolation was imple­
mented using a standard physiological database of human 
models provided in PK-Sim®. Default values for physi­
ological parameters, such as body weight, cardiac output, 
tissue-specific blood flow distribution, and volume, were 
applied to adult females (average body weight 50–60 kg; for 
each race). During the interspecies extrapolation process, 
key biochemical parameters, particularly hepatic clear­
ance and biliary clearance, were converted from mouse to 
human using an allometric scaling approach that accounted 
for differences in body mass between species. The scaling 
exponents used were 0.75 for clearance, 1 for volume of 
distribution (Vd), and − 0.25 for rate constant. Parameters 
related to biodistribution, such as the tissue-to-plasma 
Kp and the permeability coefficient, are derived through 
calculation methods based on the material properties of 
1 3

---CHUNK_BREAK---

permeability coefficient, are derived through calculation methods based on the material properties of 1 3 volume, etc.), biochemical parameters (hepatic clearance, 
etc.), Kp, and cellular permeability, and is mostly composed 
of default values provided in PK-Sim® and values based on 
literature reports (Tables 1 and 2). Based on this informa­
tion, PBPK model development was performed on an ini­
tial mouse model, and parameter optimization and model 
refinement were iteratively performed through comparison 
with observed data input. This process is schematically 
represented by the solid and dashed arrows in Fig. 1, and 
is iteratively adjusted to maximize the agreement between 
observed and model-predicted values. The next step, PBPK 
model validation, evaluates how well the developed model 
quantitatively reproduces the time-concentration curve 
from independent external experimental data. Model valid­
ity is confirmed through model fit and predictive power ver­
ification. The validated model then moves on to the PBPK 
model expansion stage, where it is extended to the human 
model through interspecific extrapolation. Physiological 
parameters are replaced with human-specific values, and 
biochemical parameters are converted through allometric 
scaling as needed. The Kp and permeability coefficient cal­
culation algorithms utilize the same calculation method to 
account for species specificity, but species-specific adjust­
ments are made based on the lipid/water composition ratio 
of each tissue. Finally, in the PBPK model application stage, 
the established human body model is used to quantitatively 
analyze the dose-exposure relationship through single and 
repeated exposure simulations and to predict tissue-level 
exposure indices (AUC, Cmax, MRT, clearance, etc.). These 
prediction results serve as the basis for evaluating tissue-
specific accumulation patterns and the potential for toxicity. 
Figure 1 structurally presents how the PBPK model can be 
applied as an integrated analysis platform to quantitatively 
predict human tissue-level cumulative exposure to toxicants 
through organic linkage between experimental toxicity data 
and numerical models, going beyond simple pharmacody­
namic predictions.
tissue distribution and body persistence of PCB-153 between 
sexes during long-term exposure. From the predicted results 
of the simulations, PK indices such as AUC, maximum con­
centration (Cmax), clearance, time to reach Cmax (Tmax), T1/2, 
mean residence time (MRT), Vd, and minimum concentra­
tion at steady state (Ctrough) were individually quantitatively 
extracted for each tissue (brain, liver, fat, skin, plasma, etc.). 
Based on these, the exposure dose and residence time char­
acteristics in major tissues in the human body were com­
pared and analyzed. These tissue-specific predictions can 
be utilized as key information for predicting the possibil­
ity of tissue accumulation and the risk of chronic toxicity 
upon repeated exposure. Furthermore, for the repeated-dose 
simulation, the model was set up based on fixed-interval 
dosing conditions, in which a fixed dose is administered at 
fixed intervals, and the model was structured to identify the 
steady-state reaching point and accumulation ratio for each 
condition. The overall model simulation and post-process­
ing analysis were performed using standard module-based 
functions that can be directly extracted from the PK-Sim® 
simulation results, which is consistent with the methods uti­
lized in existing PBPK studies.
Results
Overall workflow
Figure  1 is a flowchart comprehensively visualizing the 
development and application of the PBPK model for PCB-
153 performed in this study. The overall workflow largely 
consists of four stages: ① information input and model 
development, ② model calibration and validation, ③ inter­
species extrapolation and human model expansion, and ④ 
model application, including prediction of tissue-level con­
centrations within the human body.
First, the starting point of modeling is the information 
input, which includes the physicochemical properties of 
PCB-153 (Log P, water solubility, plasma protein bind­
ing rate, etc.), physiological parameters (tissue blood flow, 
Fig. 1  Schematic diagram of the 
development, validation, and appli­
cation processes of the PCB-153 
physiologically based pharmaco­
kinetic (PBPK) model performed 
in this study. The solid lines in 
the schematic diagram represent 
the movement flow of each major 
process, and the dotted lines repre­
sent the movement to the next step 
through the iterative processes

1 3

---CHUNK_BREAK---

lines repre­ sent the movement to the next step through the iterative processes 1 3 chemical structure containing halogen elements and the Log 
P value (7.2) reflect the high lipophilicity of PCB-153, sug­
gesting the possibility of accumulation in tissues with high 
lipid content in the body (e.g., adipose tissue). The plasma 
protein binding rate is very high at 95%, indicating that the 
free fraction of PCB-153 in the body is extremely limited, a 
factor that can significantly affect the rate of tissue diffusion 
and clearance. As for absorption-related parameters, the 
transcellular intestinal permeability was set to 5.76 cm/min 
to reflect the intestinal absorption rate in a specific organ, 
which is similar to the absorption characteristics of highly 
soluble compounds suggested in the existing literature. 
The extent of elimination by hepatic metabolism and bili­
ary excretion was set to low values (1.08 × 10–4 min⁻1 and 
9.74 × 10–5 min⁻1), respectively, considering literature-based 
data on the persistence of PCB-153 in the body, which is an 
important factor explaining that PCB-153 has a very long 
biological T1/2. Renal excretion was judged to be extremely 
minimal according to existing literature, and therefore renal 
elimination was not considered as a major route of elimina­
tion in this model. In addition, the tissue Kp values were 
calculated based on the PK-Sim standard methodology in 
PK-Sim®, taking into account the lipid and water content of 
each tissue, and these values served as key inputs for tissue-
specific exposure prediction. The dosage form information 
was applied as a solubility model based on the fact that 
highly fatty PCB-153 should be mixed with lipid substances 
to facilitate absorption in the body. All these parameters 
were configured to quantitatively reflect the in vivo kinetic 
characteristics of PCB-153 and were used as basic data for 
future tissue-level exposure prediction and repeated-dose 
simulation.
Model calibration and goodness-of-fit in mouse
Table 3 presents a summary of the final optimized model 
parameters derived through the model calibration process 
for developing the PCB-153 PBPK model in mice, and 
includes details of the parameters that were calibrated based 
on literature-based initial values to improve the predictive 
power of the model.
For the Kp, the values were set for major tissues such as 
brain, liver, adipose, and skin, and it can be confirmed that 
the calibration results are reflected by comparing them with 
literature-based values for each tissue. The Kp calculation 
method for each tissue was ultimately fixed to the same PK-
Sim standard method that was initially applied. In addition, 
cellular permeabilities related to body absorption were opti­
mized from the initially applied PK-Sim standard method 
to the charge-dependent Schmitt method. This correction is 
intended to improve the prediction accuracy of the model 
for tissue distribution and body absorption. In particular, for 
PBPK model construction and input parameters for 
PCB-153 in mouse
Table 1 comprehensively summarizes the ADME informa­
tion used as a key basis for the design of the PBPK model 
structure and initial parameter settings for PCB-153. This 
table is based on literature-based qualitative and quanti­
tative data, and each item is reflected as a key parameter 
within the model, playing a central role in setting input val­
ues for predicting the material’s in vivo behavior.
First, in terms of absorption, PCB-153 is a lipophilic sub­
stance with a Log P value of approximately 7.2, demonstrat­
ing rapid and extensive gastrointestinal absorption through 
oral administration. This high absorption rate was consid­
ered when determining the intestinal permeability coeffi­
cient and absorption rate constant within the PBPK model. 
In terms of distribution, it was emphasized that PCB-153, 
due to its high solubility, accumulates primarily in adipose 
tissue, with the lipid layer, rather than plasma, being its pri­
mary distribution site. This distribution characteristic was 
reflected in the determination of the Kp, and concentrations 
in adipose tissue in humans and rodents have been reported 
to be hundreds of times higher than in plasma (Lee et al. 
2007, 2002). Furthermore, protein binding is very high, 
with PCB-153 primarily present in plasma bound to lipo­
proteins or albumin, with a low free concentration. In terms 
of metabolism, PCB-153 has a relatively resistant struc­
ture to metabolism, which is related to the slow oxidative 
metabolism by CYP450 enzymes due to its high chloride 
substitution structure. Although PCB-153 is converted to 
hydroxylated metabolites in the liver, its metabolism is rela­
tively slow. This low intrinsic clearance value necessitates a 
conservative approach when determining hepatic clearance 
and T1/2. The excretion section emphasizes that PCB-153 is 
primarily excreted via the bile and feces, with only mini­
mal excretion via the kidneys. In experimental animal stud­
ies, 80–90% of the total administered dose is excreted via 
the hepatic-biliary-intestinal route, with some influence of 
enterohepatic circulation also reported (Kania-Korwel and 
Lehmler 2016; Peterson et al. 1976). Thus, Table 1 com­
prehensively describes the ADME characteristics of PCB-
153 in the body, serving as the foundation for establishing 
model input values and ensuring the physiological validity 
of modeling scenarios. Furthermore, this ADME informa­
tion served as a key indicator for quantitatively adjusting 
tissue distribution ratios, metabolic rates, and tissue clear­
ance within the PBPK model.
Table 2 summarizes the key initial parameter values 
applied to the human PBPK model of PCB-153 established 
in this study, which were derived from web-based databases 
(e.g., PubChem, ChemSpider), existing relevant literature, 
and the default built-in database of PK-Sim®. First, the 
1 3

---CHUNK_BREAK---

ChemSpider), existing relevant literature, and the default built-in database of PK-Sim®. First, the 1 3 (Tables 1 and 2). Therefore, fu = 0.087 applied in this model 
can be accepted as a reasonable level that is consistent with 
the structural characteristics and literature evidence, even 
considering the uncertainty of the experimentally based 
values. The key parameters related to distribution and 
clearance—such as distribution rate, hepatic and biliary 
clearance—did not differ significantly between the initial 
values and the values after model optimization, suggesting 
that the structural fit of the model (especially the clearance 
part) was high. This means that the initial model already 
had sufficient explanatory power for the physiological and 
pharmacological properties, and that during the calibration 
process, it was able to well explain the observed data with 
only fine adjustments of parameters rather than the struc­
ture itself. In summary, the results in Table 3 demonstrate 
that the model possesses structural validity and physiologi­
cal consistency, sufficiently describing the biodistribution 
and elimination kinetics without excessive parameter tun­
ing across the model. Furthermore, the adjusted physico­
chemical parameter values are optimized to a level that is 
sufficiently reliable within the literature-based numerical 
and experimental uncertainty ranges. Therefore, the PBPK 
model is considered to possess both biological validity and 
predictive reliability while maintaining high consistency 
with actual animal experimental data.
The results for visually evaluating the model’s predictive 
performance are presented in Fig. 2. This figure compares 
the observed and model-predicted values for the temporal 
the liver and adipose, the initial errors of more than three­
fold were significantly corrected to within threefold, reflect­
ing the characteristics of PCB-153’s rapid absorption and 
wide distribution among tissues. In addition, parameters 
related to the physicochemical properties of PCB-153 were 
also fine-tuned (minor optimization) through calibration. 
Log P is an important indicator reflecting the characteristics 
of PCB-153 as a highly soluble substance, and is reported 
to range from approximately 6.8 to 7.2 in web-based data­
bases (Table 2). Accordingly, the initial value in this model 
was set to 7.2, and it was ultimately optimized to 7.0, which 
was adjusted to a reasonable level within the range of theo­
retical values and literature estimates. This indicates that the 
model appropriately reflects the distribution of lipid com­
partment centers. In the case of solubility, the initial value of 
0.91 μg/L was reduced by approximately 13% to 0.79 μg/L. 
This value is still within the 20% variation range. Consid­
ering the lack of clear experimentally-based solubility data 
for PCB-153 and the fact that the initial value itself utilized 
a prediction based on molecular structure and Log P, this 
variation is considered a re-estimation within an acceptable 
range. Therefore, this can also be interpreted as a physio­
logically valid correction result. For plasma protein binding 
(fraction unbound, fu), the initial value was 0.05 (95% bind­
ing), and the optimized value was adjusted to 0.087 (91.3% 
binding). PCB-153 has been reported to exhibit high bind­
ing properties to VLDL, albumin, etc. in vivo, and previous 
studies have suggested that the total binding rate is over 90% 
Table 3  Summary of optimization of input parameters applied to establish the final physiologically based pharmacokinetic (PBPK) model of 
PCB-153
Category
Parameters
Units
Input information
Optimized
Physicochemical
Effective molecular weighta
g/mol
228.88
Lipophilicity (Log P)
NA
7.00
From the initial value of 7.2 to the final opti­
mized value of 7.00
Solubility at pH 7.0
μg/L
0.79
From the initial value of 0.91 to the final opti­
mized value of 0.79
Fraction unbound (Fu)
%
8.70
From the initial value of 5.0 to the final opti­
mized value of 8.70
Cellular permeabilities calculation
NA
Charge dependent 
Schmitt method
From the initial application PK-Sim standard to 
the final optimization Charge dependent Schmitt
Parameter m for correlation of intes­
tinal permeability (transcellular)
NA
1.11
Partition coefficients calculation
NA
PK-Sim standard 
method
Partition rate (between plasma and 
blood cells)
173.96
Elimination
Plasma clearance (liver)
1.45 × 10–5
Specific clearance (liver)
1.08 × 10–4
Plasma clearance (biliary)
1.31 × 10–5
Specific clearance (biliary)
9.74 × 10–5
NA Not applicable
a It refers to the value according to the removal of halogen elements within the structure
b This means that there was no significant change between the information applied when establishing the initial model and the information 
optimized in the final modeling process
1 3

A quantitative model fit assessment is presented in detail 
in Fig. 3. Figure 3A presents the results of a correlation anal­
ysis between the observed and predicted values. The regres­
sion line slope was approximately 1.00 and the coefficient 
of determination (R2) was over 0.90, indicating a very high 
level of fit. Figure 3B plots the distribution of residuals over 
time, confirming that there was no biased prediction ten­
dency in specific time periods or organizations, with most 
residuals falling within the ± 0.3 range. Figure 3C presents 
the results of a two-fold error analysis for each organiza­
tion and observation point over time. All data fell within the 
acceptable ± twofold error range, suggesting that the model’s 
predictive accuracy was reliable. Finally, Fig. 3D presents a 
concentration changes in brain, liver, fat, and skin tissues 
of PCB-153 after a single oral administration of 20  mg/
kg to mice. Figure 2A presents the results compared with 
95% confidence intervals, demonstrating that the observed 
values are well distributed within the predicted curves and 
confidence intervals. Figure 2B shows the results based on 
the prediction interval, confirming that most of the observed 
values fall within the range that includes the uncertainty of 
the model prediction. The VPC interval in Fig. 2C shows 
that the prediction range generated through the Monte 
Carlo-based simulation results, which reflect the uncertainty 
of the model structure and parameters, sufficiently encom­
passes the observed values.
Fig. 3  Validation results of the 
developed mouse physiologically 
based pharmacokinetic (PBPK) 
model for PCB-153. A Comparison 
of agreement between observed 
values and model predictions (solid 
line in the graph indicates perfect 
agreement between predicted and 
observed values, and the dotted 
lines indicate the 95% predic­
tion interval); B Identification of 
residual value (difference between 
model-predicted and measured 
values) patterns (dotted line in the 
graph indicates perfect agreement 
between predicted and observed 
values, and the solid arrows 
indicate the direction of the residu­
als); C Identification of two-fold 
error values for each sample point 
(dotted lines in the graph indicate 
acceptable bounds for two-fold 
error); D Histogram of residual 
value distributions

Fig. 2  Visual graphical results of the fit between the observed (after 
a single 20 mg/kg dose) and predicted values of the mouse physio­
logically based pharmacokinetic (PBPK) model for PCB-153. Dots in 
the graph represent observed values, and solid lines represent model 
predicted values. Shaded areas in the graph represent confidence or 
prediction intervals based on the model. A 95% confidence intervals 
compared to observed values; B 95% prediction intervals compared 
to observed values; C Visual predictive check intervals compared to 
observed values

1 3

---CHUNK_BREAK---

compared to observed values; C Visual predictive check intervals compared to observed values 1 3 were derived based on the sensitivity coefficient for changes 
in AUCinf or Clast, which serve as prediction indices for each 
tissue. Only parameters with an absolute value of the sensi­
tivity coefficient of 0.2 or higher among all parameters were 
selected and presented (Fig. 4). This is to conduct an analy­
sis focusing only on variables that have a substantial impact 
on the model prediction results.
First, the most sensitive parameter in Fig. 4A (AUCinf 
in brain) was ‘PCB-153: Lipophilicity (Log P)’, with the 
highest sensitivity coefficient of − 3.7. This suggests that the 
high lipid solubility of PCB-153 has a key impact on its 
accumulation and distribution in brain tissue, and reaffirms 
that lipid solubility of drugs is a major determinant, espe­
cially in tissues that must pass the blood–brain barrier, such 
as the central nervous system. In addition, ‘Fat: Volume 
fraction (lipid)’, ‘Brain: Volume fraction (lipid)’, ‘PCB-
153: Effective molecular weight’, ‘Kp (plasma-interstitial)’, 
‘Gastrointestinal transit time’, and ‘Jejunum surface area 
enhancement factor’ all showed |sensitivity|> 0.2, confirm­
ing that these physiological and physicochemical variables 
significantly affect the distribution in the brain. Similarly, in 
histogram of the residuals and a normal distribution curve, 
demonstrating that the residuals were symmetrical around 
the mean and met the assumption of a normal distribution. 
This supports the absence of systematic bias in the model 
prediction error and the overall good representation of the 
predicted values of the observed values. Overall, these 
results demonstrate that the mouse-based PCB-153 PBPK 
model developed in this study was sufficiently calibrated 
and validated to quantitatively and appropriately reflect the 
pharmacodynamic behavior in various tissues, including the 
brain, liver, skin, and fat, and suggest that it can be utilized 
as a reliable prediction platform for extrapolation to subse­
quent human models and exposure assessment applications.
Sensitivity analysis of key parameters
Figure 4 visually presents the results of the sensitivity anal­
ysis of the main parameters of the PBPK model for PCB-
153 constructed in this study, and quantitatively evaluates 
the factors affecting the variability of the predicted values 
for each target tissue. The results of the sensitivity analysis 
Fig. 4  Sensitivity analysis results for the physiologically based phar­
macokinetic (PBPK) model of PCB-153 established in this study. A 
AUCinf in brain; B AUCinf in liver; C AUCinf in skin; D AUCinf in 
plasma; E Clast in fat. AUCinf Area under the profile curve from 0 to 
infinity after PCB-153 exposure, Clast Concentration value at the last 
observation time after PCB-153 exposure

1 3

---CHUNK_BREAK---

PCB-153 exposure, Clast Concentration value at the last observation time after PCB-153 exposure 1 3 of influence on the prediction sensitivity. These analytical 
results not only predict the in vivo behavior of PCB-153, 
but also provide guidance on which parameters should be 
focused on initialization and optimization when building 
predictive models for similar highly soluble environmen­
tal residues. In particular, they can serve as important cri­
teria for prioritizing experimentally derived parameters to 
enhance model reliability.
Human PBPK model via interspecies extrapolation
In this study, we performed interspecies extrapolation to 
humans based on the developed mouse-based PBPK model, 
and constructed an extended human PBPK model based on 
human physiological parameters and body weight (average 
adult body weight 60‒70 kg; for each race). Then, based on 
the model, we simulated the temporal concentration patterns 
of PCB-153 in tissues of a population (50% male and 50% 
female, n = 100) following a single oral administration of 
20 mg/kg of PCB-153. Figure 5A shows the concentration–
time curve in target tissues using this human PBPK model. 
The simulation results showed that the concentration of 
PCB-153 in all tissues increased rapidly immediately after 
administration and then gradually stabilized. In particular, 
in adipose tissue, a tissue with high lipid content, the initial 
peak concentration (Cmax) (within 24 h) was approximately 
14.21 μg/mL on average, and the high concentration was 
maintained thereafter, increasing to 27.25 μg/mL. Liver and 
brain tissues also showed relatively high accumulation char­
acteristics, with an average Cmax of approximately 39.69 μg/
mL and 14.90 μg/mL, respectively. Skin was approximately 
14.98 μg/mL, showing an intermediate concentration dis­
tribution compared to other tissues. On the other hand, the 
concentration in plasma was very low compared to other tis­
sues, and the maximum concentration remained at approxi­
mately 0.31 ng/mL. This result is interpreted as related to 
the high lipophilicity (Log P = 7) and high protein binding 
rate (91.3%) of PCB-153, which causes it to preferentially 
distribute to lipid tissues. In addition, this result supports 
that PCB-153 is a representative lipophilic compound that is 
evenly distributed in most tissues while showing high accu­
mulation in lipid storage tissues. In this simulation, a Monte 
Carlo-based population model was applied to account for 
inter-individual variation, and the 2.5th and 97.5th percen­
tiles of concentrations for each tissue are indicated by dot­
ted lines. For adipose tissue, inter-individual variation was 
relatively large, which is believed to be due to differences 
in body fat mass and variations in related parameters within 
the population.
the analysis results of Fig. 4B (AUCinf in liver), ‘PCB-153: 
Lipophilicity (Log P)’ showed the greatest influence, and 
other distribution-related parameters such as ‘Volume frac­
tion (lipid)’ and ‘PCB-153: Kp (plasma-interstitial)’ of liver 
tissue showed sensitivity coefficients with absolute values 
ranging from 0.2 to 2. Since the liver is a high-blood flow 
tissue with a large lipid accumulation capacity, it is inter­
preted that the sensitivity of the Kp and tissue fat distribu­
tion-related factors was relatively greater in predicting the 
liver distribution of highly soluble environmental residues 
such as PCB-153. In Fig. 4C (AUCinf in skin), in addition to 
the lipid-soluble parameter (Log P), ‘Skin: Volume fraction 
(lipid)’ and ‘Skin: Fraction interstitial’ were derived with 
sensitivity coefficients of absolute values of 0.2‒1, and these 
variables had a major influence on explaining the accumula­
tion of PCB-153 in the skin. Since the skin has relatively 
low metabolic activity compared to other tissues and has a 
structure with a developed lipid layer that can function as a 
storage of substances, it is interpreted that lipid-soluble and 
skin-specific physiological factors are ranked high in the 
sensitivity items. In Fig. 4D (AUCinf in plasma), ‘PCB-153: 
Lipophilicity (Log P)’ showed the highest sensitivity with 
a sensitivity coefficient of approximately − 53. This result 
clearly suggests that the degree of lipid solubility is a key 
determining factor in the systemic exposure of PCB-153. 
This interpretation is consistent with the pharmacodynamic 
principle that highly lipid-soluble drugs extensively pen­
etrate, distribute, and accumulate from the blood to adipose 
tissues. In addition, ‘PCB-153: Effective molecular weight’, 
‘Albumin: Ontogeny factor’, and ‘Fat fraction vascular’ 
also had an absolute value of sensitivity coefficient of 0.2 
or higher, affecting the prediction of blood concentration. 
Finally, in Fig. 4E (Clast in fat), various parameters such as 
‘Log P’, ‘Fat: Volume fraction (lipid)’, ‘Bone: Volume’, 
and ‘PCB-153: Solubility’ showed sensitivity coefficients 
in the range of 0.2‒5, and in particular, ‘Log P’ was evalu­
ated as the variable with the greatest influence on predict­
ing the final concentration in fat tissue, with a value of 
approximately + 4.8. This is closely related to the long-term 
accumulation characteristics of PCB-153, a highly soluble 
environmental pollutant, in fat tissue, and can be considered 
a key parameter for model prediction.
Overall, the sensitivity analysis results commonly con­
firmed that Log P (lipophilicity) showed the highest sensi­
tivity for most tissue prediction values (AUCinf and Clast), 
which served as evidence that the biodistribution dynam­
ics of high-lipophilic chemicals are critically influenced 
by lipophilicity. In addition, variables related to gastroin­
testinal absorption (surface area of the jejunum and ileum, 
transit time, solubility), tissue volume and blood flow, 
protein-binding factors, and total blood component compo­
sition (hematocrit) were also found to have a certain level 
1 3

---CHUNK_BREAK---

blood component compo­ sition (hematocrit) were also found to have a certain level 1 3 not statistically significant. In particular, when compared 
with weight-normalized values, the difference was further 
reduced, confirming that the difference in the body distribu­
tion of PCB-153 by gender was not significant.
Meanwhile, since continuous exposure to PCB-153 is 
more common than single exposure in actual environmen­
tal exposure, Fig. 7 presents the results of a multiple-dose 
simulation performed according to a scenario of repeated 
oral administration at 24 h intervals. This was because the 
recently reported RfD for PCB-153 is presented in daily 
units and because it is a standard dosage applied to continu­
ous exposures to substances in general (Ermler and Korten­
kamp 2022). Figure 7A shows the predicted concentration 
profiles in each tissue for up to 100 days of repeated admin­
istration, a total of 2400 h, and clearly shows a pattern of 
reaching a steady-state in all tissues over time. In particular, 
gradual accumulation with the highest concentration was 
observed in adipose tissue, while relatively low concentra­
tions were maintained in plasma. Based on these simulation 
results, Fig.  7B summarizes the distribution of PCB-153 
concentrations in each tissue in the form of a box plot at 
steady-state point in the 2,376–2,400 h period after repeated 
administration, and among them, adipose tissue showed 
the highest concentration level on average (up to approxi­
mately 2.5  ng/mL or more), whereas plasma showed the 
lowest concentration (approximately 0.004 pg/mL or less). 
Finally, Fig.  7C presents the predicted results converted 
to ng/g lipid units by applying the average value of blood 
lipid concentration (based on 650 mg/dL) for the purpose 
of comparing the PCB-153 concentration in plasma with 
the actual biomonitoring results. As a result, the predicted 
steady-state average concentration of PCB-153 converted to 
the standard plasma lipid unit of a normal adult was approx­
imately 0.0003 ng/g lipid, which was much lower than the 
actual reported range of blood PCB-153 concentrations in 
Simulation of human tissue exposure at RfD
This paper presents various simulation results utilizing a 
human PBPK model developed to quantitatively understand 
how external exposure to PCB-153 at the RfD level is dis­
tributed and maintained in major tissues within the human 
body. This study applied an RfD value of 0.0058 µg/kg/day, 
proposed through a systematic review of the existing litera­
ture, based on recent research findings specifically focus­
ing on semen quality degradation as a key health impact 
indicator.
First, Fig. 5B visualizes the changes in PCB-153 con­
centrations in different tissues up to 336 h after a single oral 
dose of RfD in a mixed-gender group (n = 100, 50 males and 
50 females). All tissues showed a rapid initial absorption 
followed by a relatively gradual decline, with the highest 
level of accumulation and a tendency to persist, particularly 
in adipose tissue. The mean predicted curve (solid line) and 
the inter-individual variation (dotted line) within the 2.5–
97.5% range clearly show the characteristics of the concen­
tration distribution at the group level. Similar concentration 
profiles were observed in the liver, brain, and skin, but the 
lowest concentration level was consistently maintained in 
plasma.
Figure 6 compares the predicted concentration distribu­
tions separately in female (A) and male (B) groups under 
the same RfD single-dose conditions. Each gender group 
consisted of n = 100, and a population module was used 
that applied an average body weight range of 50–60 kg for 
females and 60–80  kg for males. The simulation results 
showed that both groups showed the same overall pattern of 
high concentration accumulation in adipose tissue and low 
concentration maintenance in plasma. The box plot com­
parison results in Fig. 6C also suggested that the difference 
in concentration distribution between the two groups was 
Fig. 5  Results of simulation of the population (n = 100, comprised of 
50% male and 50% female) pharmacokinetic (PK) profiles among 
target tissues following a single oral administration of 20 mg/kg (A) 
or reference dose (RfD, B) of PCB-153 using the human physiologi­
cally based pharmacokinetic (PBPK) model of PCB-153 established 
in this study. The solid lines in the graph represent the group mean 
values predicted by the model, while the dotted lines represent the val­
ues corresponding to 97.5% (upper) and 2.5% (lower) of the groups, 
respectively

1 3

human body, providing a scientific basis for predicting body 
accumulation characteristics, particularly the potential for 
accumulation in adipose tissue. This can serve as basic data 
for future exposure assessments and health risk predictions.
the general public (McLachlan et al. 2018; ME 2024; Unde­
man et al. 2018). Thus, the simulation results demonstrate 
that exposure at the proposed RfD level exhibits consistent 
distribution characteristics across major tissues within the 
Fig. 7  Results of simulation of the 
population (n = 100, comprised of 
50% male and 50% female) phar­
macokinetic (PK) profiles among 
target tissues following multiple 
oral administrations of reference 
dose (RfD) of PCB-153 using 
the human physiologically based 
pharmacokinetic (PBPK) model 
of PCB-153 established in this 
study. The solid lines in the graph 
represent the group mean values 
predicted by the model, while the 
shaded regions represent the values 
corresponding to 2.5‒97.5% of the 
groups, respectively. A PK profile 
results based on model simula­
tion; B Comparison of concentra­
tion distributions in each target 
tissue at steady state; C Predicted 
distribution of steady-state plasma 
concentrations

Fig. 6  Comparison of the phar­
macokinetic (PK) profile simula­
tion results among target tissues 
following a single oral administra­
tion of PCB-153 at the reference 
dose (RfD) for female and male 
populations (n = 100), respectively, 
in the human physiologically based 
pharmacokinetic (PBPK) model of 
PCB-153 established in this study. 
A Model simulation results for 
female population; B Model simu­
lation results for male population; 
C Boxplot comparison of PCB-153 
concentration distributions between 
female and male populations. The 
solid lines in the graph represent 
the group mean values predicted by 
the model, while the dotted lines 
represent the values corresponding 
to 97.5% (upper) and 2.5% (lower) 
of the groups, respectively

1 3

---CHUNK_BREAK---

the values corresponding to 97.5% (upper) and 2.5% (lower) of the groups, respectively 1 3 Table 5 also presents the key PK parameter values under 
repeated exposure conditions based on the RfD, and these 
values reflect the within-population variability, including 
the 2.5–97.5% confidence intervals. In the case of adi­
pose tissue (in the continuous exposure scenario at 24-h 
intervals), it was impossible to derive parameters such as 
AUCinf, clearance, MRT, T1/2, and Vd due to the continu­
ous PCB-153 tissue accumulation profile characteristics. 
However, the steady-state Ctrough was the highest among the 
target tissues, with an average of 1.76 ng/mL. These results 
once again demonstrate that adipose tissue is the main 
accumulation site of PCB-153, supporting the importance 
of adipose tissue in the in vivo PKs of highly soluble sub­
stances. In plasma, the average AUCinf was 0.34 pg∙h/mL, 
showing a relatively low accumulation pattern compared to 
target tissues such as brain, fat, liver, and skin. In terms of 
T1/2, the estimated values in all target tissues except fat were 
very long, averaging 8,400–10,500 h, and the MRT was also 
long, averaging 12,000–15,000 h. The estimated clearance 
in brain, liver, and skin tissues was very low, averaging 
0.003–0.005 mL/min/kg. Overall, these strongly suggested 
the long-term persistence and low clearance of PCB-153 in 
the body, and were consistent with the qualitative character­
ization information known from previous reports (Grand­
jean et al. 2008; Lindell 2012).
Additionally, this study also presents a schematic dia­
gram of the risk assessment approach using the established 
human PBPK model, as shown in Fig. 8. This schematic 
Interpretation of tissue-specific toxicokinetic 
implications
As a result of confirming the distribution and accumula­
tion characteristics of PCB-153 in each tissue based on the 
steady state standard obtained through multiple repeated 
exposure simulations (Table  4), the Kp in adipose tissue 
was the highest at an average of 4961.45, followed by the 
brain (976.96), skin (639.89), liver (522.61), and plasma 
(1.0). This suggests that PCB-153, which has high solubility 
characteristics, may be preferentially distributed to adipose 
tissue and accumulate in the body for a long time. In partic­
ular, accumulation in inactive tissues such as adipose tissue 
has toxicodynamic implications in that it delays the onset 
of toxic effects while increasing the possibility of long-term 
retention in the body.
Table 4  Kp values of PCB-153 to target tissues at steady state follow­
ing multiple exposures (24 h dosing interval of RfD) using the human 
physiologically based pharmacokinetic (PBPK) model of PCB-153 
established in this study
Tissue Kp mean
Kp 2.5% of population
Kp 97.5% of population
Brain
976.96
1054.57
887.95
Fat
4961.45
5725.51
3979.19
Liver
522.61
567.50
472.46
Skin
639.89
690.60
581.51
RfD Reference dose, Kp Tissue distribution coefficient (calculated as 
the ratio between the concentration value in each tissue and the con­
centration value in plasma)
Table 5  Estimated pharmacokinetic (PK) parameter values from model simulations based on the previously reported RfD of PCB-153 in the 
human physiologically based pharmacokinetic (PBPK) model of PCB-153 established in this study
Parameter
Unit
Brain
Fat
Liver
Plasma
Skin
AUCinf
ng·h/mL
40.72 
[17.14‒120.66]
NA
26.53 
[10.53‒78.86]
3.36E−4 
[1.20E−4‒1.15E−3]
30.32 
[12.15‒91.31]
AUCall
ng·h/mL
1.44 [0.96‒2.23]
5.23 [3.67‒7.22]
0.84 [0.54‒1.26]
1.00E−5 
[6.14E−6‒1.63E−5]
0.96 [0.66‒1.50]
Cmax
ng/mL
1.17E−2 
[1.04E−2‒1.28E−2]
1.77E−2 
[1.18E−2‒2.55E−2]
4.04E−2 
[2.81E−2‒5.02E−2]
3.53E−7 
[2.41E−7‒5.20E−7]
1.21E−2 
[1.12E−2‒1.31E−2]
Total body 
clearance/F
mL/min/kg
3.17E−3 
[8.10E−4‒5.71E−3]
NA
4.98E−3 
[1.24E−3‒9.27E−3]
414.23 [85.04‒812.16]
4.35E−3 
[1.07E−3‒8.03E−3]
MRT
h
1.20E4 
[4.17E3‒3.00E4]
NA
1.50E4 
[4.81E3‒3.85E4]
1.49E4 [4.77E3‒3.84E4]
1.38E4 
[4.52E3‒3.54E4]
Tmax
h
9.43 [6.50‒12.38]
NA
1.44 [1.15‒1.93]
0.71 [0.40‒1.25]
5.12 [3.62‒6.75]
T1/2
h
8.40E3 
[2.95E3‒2.08E4]
NA
1.05E4 
[3.40E3‒2.68E4]
1.04E4 [3.37E3‒2.67E4]
9.66E3 
[3.20E3‒2.46E4]
Vd (plasma)/F
mL/kg
NA
NA
NA
2.82E8 [1.44E8‒4.61E8]
NA
Ctrough
ng/mL
0.34 [0.21‒0.57]
1.76 [1.17‒2.55]
0.18 [0.11‒0.30]
2.23E−6 
[1.27E−6‒4.08E−6]
0.22 [0.14‒0.37]
Parameter values are presented as ‘Mean [range 2.5‒97.5% of population]’
RfD Reference dose, NA Not applicable, AUCinf Area under the curve from 0 to infinity after administration, AUCall Area under the curve from 
0 to the observation time after administration, Cmax Maximum concentration, F Bioavailability, MRT Mean residence time, Tmax Time to reach 
the maximum concentration, T1/2 Half-life, Vd Volume of distribution, Ctrough Lowest concentration at steady state after multiple doses
a This is confirmed to be derived based on mouse PK experimental data
b This is confirmed by estimates obtained through modeling
c Rough estimate
1 3

---CHUNK_BREAK---

data b This is confirmed by estimates obtained through modeling c Rough estimate 1 3 tissues, such as fat, liver, brain, skin, and plasma, beyond the 
general single environment or limited tissue levels of exist­
ing hazardous substances. It is differentiated from existing 
universal models in that it presents results that reflect inter-
individual (including gender) variations within a population 
through population-based simulation. The overall model 
architecture, including the compartmental structure and 
flow paths, was implemented using the default whole-body 
PBPK template of PK-Sim®, comprising major organs (e.g., 
adipose tissue, liver, brain, skin, etc.) interconnected by 
physiological blood and lymph flows.
Simulation results showed that, under a single oral expo­
sure of 20 mg/kg, adipose tissue exhibited an exceptionally 
high distribution (mean Kp = 795,725 at 336 h), followed by 
brain (151,257), skin (98,656), liver (79,633), and plasma 
(1.0) (Fig.  5). This adipose tissue-centered accumulation 
pattern is interpreted as being due to the physicochemical 
properties of PCB-153, such as its high solubility (Log P of 
approximately 7.0; Table 3), which emphasizes its consid­
erably long T1/2 and limited biological clearance (Table 5). 
This is consistent with previous animal studies that have 
reported similar results, which indicate that PCB-153 can 
persist in fat for years (Klocke and Lein 2020; Lee et al. 
2007, 2002). The results of this study represent one of the 
first examples to numerically quantify this effect at the 
human level.
Meanwhile, in the simulation results for repeated admin­
istration conditions based on the RfD, which is the human 
health risk assessment standard, the AUCinf of brain tissue 
at steady state was derived as an average of 40.72 ng·h/mL, 
followed by skin (30.32 ng·h/mL), liver (26.53 ng·h/mL), 
and plasma (0.34 pg·h/mL) (Table 5). Although the AUCinf 
of adipose tissue could not be estimated to the infinite range 
due to the profile characteristics, when calculated based 
diagram illustrates how the PBPK model can be used for 
risk assessment by linking human biomonitoring data based 
on internal exposure. The first approach is to set the exist­
ing RfD value as the model input, predict the corresponding 
concentration level in the target tissue (e.g., blood lipid stan­
dardized concentration), and compare this with the actual 
biomonitoring value to evaluate the potential risk of internal 
exposure based on the RfD standard. The second approach, 
conversely, applies biomonitoring data as output from the 
PBPK model, derives the external exposure required to 
induce the corresponding internal exposure through reverse 
dosimetry, and then estimates the safety of exposure by 
comparing this exposure to the RfD reference value. This 
structure is designed to significantly contribute to quanti­
tative risk assessment, particularly in calculating external 
exposures that reflect population-specific characteristics and 
estimating margins of safety. Consequently, the tissue-spe­
cific Kp values and PK parameters derived from this study 
can be used as basis for predicting the toxicity sensitivity 
and biological response of each tissue beyond the simple 
degree of material accumulation, and the established human 
PBPK model has shown high utility as a quantitative sup­
port system for future biomonitoring-based risk assessment.
Discussion
This study aimed to establish a PBPK model based on ani­
mal experimental results for PCB-153, a highly chlorinated 
polychlorinated biphenyl, and to quantitatively predict 
toxicokinetic exposure at the level of target tissues in the 
human body through interspecies extrapolation between 
animals and humans. In particular, this model was designed 
to predict body accumulation trends in several major target 
Fig. 8  Schematic diagram of an approach to population exposure risk 
assessment utilizing human biomonitoring data for PCB-153 using an 
established human physiologically based pharmacokinetic (PBPK) 
model for PCB-153. The blue arrow paths in the schematic represent 
the risk estimation process through the transition flow from internal 
exposure-based starting values to external exposure estimates, while 
the red arrow paths represent the exposure risk estimation process 
through the transition flow from external exposure-based starting val­
ues to internal exposure estimates. The gray arrow paths in the sche­
matic represent the exposure risk estimation process through the direct 
comparison between monitored internal exposure values and model-
based estimated internal exposures

1 3

---CHUNK_BREAK---

direct comparison between monitored internal exposure values and model- based estimated internal exposures 1 3 Furthermore, the RfD, the external exposure criterion 
applied in the single and repeated exposure simulations con­
ducted in this study, was based on values presented in recent 
literature (Ermler and Kortenkamp 2022), and the RfD was 
calculated by setting sperm function impairment as the main 
toxicity indicator in animal experiments. In this study, the 
predicted PCB-153 concentrations in major target tissues 
(fat, brain, liver, skin, etc.) in humans as well as in plasma 
were significantly lower (Fig.  7) than the actual internal 
exposure levels reported in previously reported human 
blood biomonitoring data (Crinnion 2010; McLachlan et al. 
2018; ME 2024; Undeman et al. 2018). This implies that the 
applied RfD itself may have been estimated conservatively 
or excessively low compared to the actual toxicity level 
in humans. In particular, considering the characteristics 
of highly soluble and bioaccumulative substances such as 
PCB-153, there is concern that the RfD derived solely from 
extrapolated animal toxicity data may not adequately reflect 
the actual human exposure situation. Therefore, future stud­
ies will require resetting the RfD based on more precise 
toxicodynamic and pharmacodynamic scientific evidence, 
and based on this, it is expected that a more reliable risk 
assessment of PCB-153 will be possible through linkage 
with human biomonitoring data.
Conclusion
This study established a human PBPK model for the envi­
ronmental persistent pollutant PCB-153 and quantitatively 
predicted tissue-level accumulation patterns and exposure 
based on this model, thereby presenting a quantitative tool 
that can overcome the limitations of existing risk assess­
ment approaches. In particular, adipose tissue exhibited a 
distinct accumulation characteristic, with an average Kp of 
over 79,633 among target tissues after a single oral dose of 
20 mg/kg. Even under repeated exposure conditions (RfD), 
the average Kp in adipose tissue was the highest at steady 
state, at 4,961, numerically confirming the possibility of 
long-term retention, particularly in high-adipose tissue. Fur­
thermore, this model demonstrated the feasibility of realis­
tic exposure predictions considering diverse physiological 
characteristics within the human body through Monte Carlo 
simulations that reflected interindividual variation within a 
population. These results not only deepen our understand­
ing of the toxicokinetics of PCB-153 but also provide a fea­
sible framework for top-down and bottom-up quantitative 
risk assessment strategies based on internal exposure, dem­
onstrating significant academic and practical value. This 
study can be used as scientific basis for the future assess­
ment of human impact and establishment of safety stan­
dards for highly soluble environmental pollutants, including 
only on AUCall (AUC to observed time not infinity), it was 
the highest among the target tissues at 5.23 ng·h/mL, which 
was approximately four times that of brain tissue. These 
results suggest that there is a sufficient possibility of long-
term accumulation centered on fat even under the RfD stan­
dard, and support the need for a conservative interpretation 
in risk assessment, as it is difficult to rule out the possibility 
of long-term toxicity due to tissue accumulation even at low 
exposure doses.
Furthermore, this study schematically illustrates the 
potential expansion of this PBPK model into a quantitative 
risk assessment tool (Fig. 8). In addition to the existing RfD-
based top-down approach, a bottom-up (reverse dosimetry) 
approach based on biomonitoring data can be used to predict 
external exposure equivalent to internal exposure, thereby 
quantifying the individual margin of safety. This demon­
strates the strength of the PBPK model in supplementing the 
scientific validity of toxicity risk assessments in situations 
where existing qualitative or quantitative data are limited.
However, this study also has several limitations. First, 
although the metabolic pathway of PCB-153 mostly 
involves Phase I metabolism (CYP450 enzymes) and Phase 
II conjugation metabolism in the liver, information on the 
precise metabolic rate or concentration of metabolites pro­
duced in humans is lacking. Therefore, the metabolic rate 
in this model was set to “minimal metabolism” based on 
previously reported material characteristic information 
(Grandjean et al. 2008; Lindell 2012). This limits its exten­
sion to the assessment of the degree of polymorphism in 
specific metabolite production and toxicity phenotypes. 
Second, although prediction of lipid distribution is impor­
tant for the PK properties of high-soluble substances, there 
is a practical limitation in that there is a significant lack of 
human biomonitoring data that can be compared with the 
values measured in adipose tissue in actual clinical settings. 
To address these limitations, future research emphasizes the 
need for personalized PBPK modeling, which incorporates 
quantitative analysis of specific metabolites or reflects indi­
vidual physiological indicators such as body fat percent­
age. Furthermore, comparative evaluations with other PCB 
congeners and integration with mixture toxicity models will 
be the next steps to better reflect real-world environmental 
exposure scenarios. In conclusion, this study successfully 
extrapolated a human PBPK model from animal experi­
mental data, providing quantitative exposure predictions at 
the target tissue level and risk assessment information that 
takes into account population variation, making significant 
academic and policy contributions. In particular, the toxico­
kinetic accumulation characteristics centered on adipose tis­
sue can serve as important supporting data for future studies 
on chronic health effects and the establishment of protective 
limits following PCB-153 exposure.
1 3

---CHUNK_BREAK---

on chronic health effects and the establishment of protective limits following PCB-153 exposure. 1 3 Glauert HP, Tharappel JC, Lu Z et al (2008) Role of oxidative stress 
in the promoting activities of PCBs. Environ Toxicol Pharmacol 
25(2):247–250. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​t​a​p​.​2​0​0​7​.​1​0​.​0​2​5
Grandjean P, Budtz-Jørgensen E, Barr DB, Needham LL, Weihe 
P, Heinzow B (2008) Elimination half-lives of polychlori­
nated biphenyl congeners in children. Environ Sci Technol 
42(18):6991–6996. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​2​1​/​e​s​8​0​0​7​7​8​q
Grilo TF, Cardoso PG, Pato P, Duarte AC, Pardal MA (2014) Uptake 
and depuration of PCB-153 in edible shrimp Palaemonetes vari­
ans and human health risk assessment. Ecotoxicol Environ Saf 
101:97–102. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​c​o​e​n​v​.​2​0​1​3​.​1​2​.​0​2​0
Jones KC, de Voogt P (1999) Persistent organic pollutants (POPs): 
state of the science. Environ Pollut 100(1):209–221. ​h​t​t​p​s​:​/​/​d​o​i​.​o​
r​g​/​1​0​.​1​0​1​6​/​S​0​2​6​9​-​7​4​9​1​(​9​9​)​0​0​0​9​8​-​6
Kania-Korwel I, Lehmler H-J (2016) Chiral polychlorinated biphe­
nyls: absorption, metabolism and excretion—a review. Environ 
Sci Pollut Res 23(3):2042–2057. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​1​1​3​5​
6​-​0​1​5​-​4​1​5​0​-​2
Klocke C, Lein PJ (2020) Evidence implicating non-dioxin-like con­
geners as the key mediators of polychlorinated biphenyl (PCB) 
developmental neurotoxicity. Int J Mol Sci 21(3):1013. ​h​t​t​p​s​:​/​/​d​o​
i​.​o​r​g​/​1​0​.​3​3​9​0​/​i​j​m​s​2​1​0​3​1​0​1​3
Lee SK, Ou YC, Andersen ME, Yang RSH (2007) A physiologically 
based pharmacokinetic model for lactational transfer of PCB 153 
with or without PCB 126 in mice. Arch Toxicol 81(2):101–111. ​h​
t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​0​0​2​0​4​-​0​0​6​-​0​1​3​0​-​0
Lee SK, Ou YC, Yang RSH (2002) Comparison of pharmacokinetic 
interactions and physiologically based pharmacokinetic modeling 
of PCB 153 and PCB 126 in nonpregnant mice, lactating mice, 
and suckling pups. Toxicol Sci 65(1):26–34. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​
0​9​3​/​t​o​x​s​c​i​/​6​5​.​1​.​2​6
Lindell B (2012) 146. Polychlorinated biphenyls (PCBs). Arbets-och 
miljömedicin, Göteborgs universitet
McLachlan MS, Undeman E, Zhao F, MacLeod M (2018) Predict­
ing global scale exposure of humans to PCB 153 from historical 
emissions. Environ Sci Process Impacts 20(5):747–756. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​1​0​3​9​/​C​8​E​M​0​0​0​2​3​A
ME (2024) Ministry of Environment, Disclosure of the Results of the 
5th National Environmental Health Basic Survey, Accessed on 
Aug. 22, ​h​t​t​p​s​:​/​/​m​e​.​g​o​.​k​r​/​h​o​m​e​/​w​e​b​/​b​o​a​r​d​/​r​e​a​d​.​d​o​?​m​e​n​u​I​d​=​1​0​5​
2​5​&​b​o​a​r​d​I​d​=​1​7​1​6​9​3​0​&​b​o​a​r​d​M​a​s​t​e​r​I​d​=​1. In.
Organization WH (2010) Persistent organic pollutants: impact on child 
health Persistent organic pollutants: impact on child health.
Patel MP, Patel KM, Vhora SZ, Gajjar AK, Patel JK, Patel AK (2025) 
Model-based pharmacokinetic approaches basics and clinical 
applications of drug disposition in special populations. p 11–51
PCB-153, Accessed on Aug. 20, ​h​t​t​p​s​:​/​/​w​w​w​.​c​h​e​m​s​p​i​d​e​r​.​c​o​m​/​C​h​e​m​i​c​
a​l​-​S​t​r​u​c​t​u​r​e​.​3​3​9​8​3​.​h​t​m​l (2025).
Peterson RE, Seymour JL, Allen JR (1976) Distribution and biliary 
excretion of polychlorinated biphenyls in rats. Toxicol Appl Phar­
macol 38(3):609–619. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​0​0​4​1​-​0​0​8​X​(​7​6​)​9​0​
1​9​1​-​5
PubChem (2025) 2,2',4,4',5,5'-Hexachlorobiphenyl (compound), 
Accessed on Aug. 20, ​h​t​t​p​s​:​/​/​p​u​b​c​h​e​m​.​n​c​b​i​.​n​l​m​.​n​i​h​.​g​o​v​/​c​o​m​p​o​u​
n​d​/​3​7​0​3​4​#​s​e​c​t​i​o​n​=​C​o​m​p​u​t​e​d​-​P​r​o​p​e​r​t​i​e​s. doi:​h​t​t​p​s​:​/​/​p​u​b​c​h​e​m​.​n​c​
b​i​.​n​l​m​.​n​i​h​.​g​o​v​/​c​o​m​p​o​u​n​d​/​3​7​0​3​4​#​s​e​c​t​i​o​n​=​C​o​m​p​u​t​e​d​-​P​r​o​p​e​r​t​i​e​s
Ritter R, Scheringer M, MacLeod M, Moeckel C, Jones KC, Hun­
gerbühler K (2011) Intrinsic human elimination half-lives of 
polychlorinated biphenyls derived from the temporal evolution 
of cross-sectional biomonitoring data from the United Kingdom. 
Environ Health Perspect 119(2):225–231. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​2​8​
9​/​e​h​p​.​1​0​0​2​2​1​1
Rodriguez EA, Li X, Lehmler H-J, Robertson LW, Duffel MW 
(2016) Sulfation of lower chlorinated polychlorinated biphenyls 
increases their affinity for the major drug-binding sites of human 
PCB-153, and is significant as a case that demonstrates the 
practical applicability of PBPK-based quantitative toxicity 
assessment.
Acknowledgements  This work was supported by a Research promo­
tion program of SCNU. This research was also supported by the Basic 
Science Research Program through the National Research Founda­
tion of Korea (NRF) funded by the Ministry of Education (RS-2023-
00245453).
Author contributions  Ji-Hun Jang: Conceptualization, Investigation, 
Methodology, Funding acquisition, Formal analysis, Data curation, 
Software, Writing—Original draft preparation, Reviewing and Edit­
ing; Seung-Hyun Jeong: Conceptualization, Investigation, Method­
ology, Project administration, Funding acquisition, Formal analysis, 
Supervision, Data curation, Software, Writing—Original draft prepa­
ration, Reviewing and Editing.
Data availability  All data and related materials are accessible in this 
manuscript.
Declarations
Conflict of interest  The authors have no conflicts of interest relevant 
to this study to disclose.
Ethical approval  Not applicable.
Consent to participate  Not applicable.
Consent for publication  Not applicable.
Ahmad I, Weng J, Stromberg AJ, Hilt JZ, Dziubla TD (2019) Fluo­
rescence based detection of polychlorinated biphenyls (PCBs) in 
water using hydrophobic interactions. Analyst 144(2):677–684. ​h​
t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​3​9​/​C​8​A​N​0​0​8​6​7​A
Chain EPoCitF (2015) Scientific opinion on the risks for human health 
related to the presence of tetrahydrocannabinol (THC) in milk 
and other food of animal origin. EFSA J 13(6):4141, ​h​t​t​p​s​:​/​/​d​o​i​.​o​
r​g​/​1​0​.​2​9​0​3​/​j​.​e​f​s​a​.​2​0​1​5​.​4​1​4​1
Crinnion WJ (2010) The CDC fourth national report on human expo­
sure to environmental chemicals: what it tells us about our toxic 
burden and how it assists environmental medicine physicians. 
Altern Med Rev 15(2):101–109
Dahl SG, Aarons L, Gundert-Remy U et al (2010) Incorporating physi­
ological and biochemical mechanisms into pharmacokinetic-
pharmacodynamic models: a conceptual framework. Basic Clin 
Pharmacol Toxicol 106(1):2–12. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​1​/​j​.​1​7​4​2​-​7​
8​4​3​.​2​0​0​9​.​0​0​4​5​6​.​x
Ermler S, Kortenkamp A (2022) Systematic review of associations of 
polychlorinated biphenyl (PCB) exposure with declining semen 
quality in support of the derivation of reference doses for mixture 
risk assessments. Environ Health 21(1):94. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​8​
6​/​s​1​2​9​4​0​-​0​2​2​-​0​0​9​0​4​-​5
Ferrante MC, Amero P, Santoro A et al (2014) Polychlorinated biphe­
nyls (PCB 101, PCB 153 and PCB 180) alter leptin signaling and 
lipid metabolism in differentiated 3T3-L1 adipocytes. Toxicol 
Appl Pharmacol 279(3):401–408. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​t​a​a​p​.​
2​0​1​4​.​0​6​.​0​1​6
1 3

---CHUNK_BREAK---

and lipid metabolism in differentiated 3T3-L1 adipocytes. Toxicol Appl Pharmacol 279(3):401–408. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​t​a​a​p​.​ 2​0​1​4​.​0​6​.​0​1​6 1 3 Weijs L, Yang RSH, Covaci A, Das K, Blust R (2010) Physiologically 
based pharmacokinetic (PBPK) models for lifetime exposure to 
PCB 153 in male and female Harbor porpoises (Phocoena pho­
coena): model development and evaluation. Environ Sci Technol 
44(18):7023–7030. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​2​1​/​e​s​1​0​1​6​8​8​h
Publisher’s Note  Springer Nature remains neutral with regard to juris­
dictional claims in published maps and institutional affiliations.
Springer Nature or its licensor (e.g. a society or other partner) holds 
exclusive rights to this article under a publishing agreement with the 
author(s) or other rightsholder(s); author self-archiving of the accepted 
manuscript version of this article is solely governed by the terms of 
such publishing agreement and applicable law.
serum albumin. Environ Sci Technol 50(10):5320–5327. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​1​0​2​1​/​a​c​s​.​e​s​t​.​6​b​0​0​4​8​4
Safe SH (1994) Polychlorinated Biphenyls (PCBs): environmental 
impact, biochemical and toxic responses, and implications for 
risk assessment. Crit Rev Toxicol 24(2):87–149. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​3​1​0​9​/​1​0​4​0​8​4​4​9​4​0​9​0​4​9​3​0​8
Sandu MA, Preda M, Tanase V, Mihailescu D, Virsta A, Ivanescu V 
(2025) Trends in polychlorinated biphenyl contamination in 
Bucharest’s urban soils: a two-decade perspective (2002–2022). 
Processes 13(5):1357. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​9​0​/​p​r​1​3​0​5​1​3​5​7
Seelbach M, Chen L, Powell A et al (2010) Polychlorinated biphenyls 
disrupt blood–brain barrier integrity and promote brain metastasis 
formation. Environ Health Perspect 118(4):479–484. ​h​t​t​p​s​:​/​/​d​o​i​.​o​
r​g​/​1​0​.​1​2​8​9​/​e​h​p​.​0​9​0​1​3​3​4
Undeman E, Brown TN, McLachlan MS, Wania F (2018) Who in 
the world is most exposed to polychlorinated biphenyls? Using 
models to identify highly exposed populations. Environ Res Lett 
13(6):064036. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​8​8​/​1​7​4​8​-​9​3​2​6​/​a​a​c​5​f​e
1 3