A human life-stage physiologically based pharmacokinetic and
pharmacodynamic model for chlorpyrifos: Development and validation
Jordan Ned Smith a,⇑, Paul M. Hinderliter a, Charles Timchalk a, Michael J. Bartels b, Torka S. Poet a
a Battelle, Paciﬁc Northwest Division, Richland, WA 99354, USA
b Dow Chemical Company, Midland, MI, USA
a r t i c l e
i n f o
Article history:
Received 28 March 2013
Available online 4 November 2013
Keywords:
Pharmacokinetics
Pesticide
Life-stage sensitivity
a b s t r a c t
Sensitivity to some chemicals in animals and humans are known to vary with age. Age-related changes in
sensitivity to chlorpyrifos have been reported in animal models. A life-stage physiologically based phar-
macokinetic and pharmacodynamic (PBPK/PD) model was developed to predict disposition of chlorpyri-
fos and its metabolites, chlorpyrifos-oxon (the ultimate toxicant) and 3,5,6-trichloro-2-pyridinol (TCPy),
as well as B-esterase inhibition by chlorpyrifos-oxon in humans. In this model, previously measured age-
dependent metabolism of chlorpyrifos and chlorpyrifos-oxon were integrated into age-related descrip-
tions of human anatomy and physiology. The life-stage PBPK/PD model was calibrated and tested against
controlled adult human exposure studies. Simulations suggest age-dependent pharmacokinetics and
response may exist. At oral doses P0.6 mg/kg of chlorpyrifos (100- to 1000-fold higher than environmen-
tal exposure levels), 6 months old children are predicted to have higher levels of chlorpyrifos-oxon in
blood and higher levels of red blood cell cholinesterase inhibition compared to adults from equivalent
doses. At lower doses more relevant to environmental exposures, simulations predict that adults will
have slightly higher levels of chlorpyrifos-oxon in blood and greater cholinesterase inhibition. This model
provides a computational framework for age-comparative simulations that can be utilized to predict
chlorpyrifos disposition and biological response over various postnatal life stages.
 2013 Elsevier Inc. All rights reserved.
1. Introduction
For some chemical exposures including pesticides, children may
have different responses than adults (Bruckner, 2000), and thus an
increased emphasis has been placed on evaluating effects of chem-
ical exposures in different age groups. Mechanisms of absorption,
distribution, metabolism, and excretion all develop at different
rates, which could lead to age-dependent discrepancies in both
pharmacokinetics and pharmacodynamics (US EPA, 2006; US
NRC, 1993). In addition, it has been suggested that variable degrees
of increased susceptibility exist in young animals compared to
adults from chlorpyrifos exposures (Marty et al., 2012; Pope
et al., 1991; Timchalk et al., 2006; Vidair, 2004; Whitney et al.,
1995; Zheng et al., 2000).
Chlorpyrifos (CPF) is a broad spectrum organophosphate insec-
ticide used in crop agriculture. Once absorbed in mammals, cyto-
chrome P450 enzymes metabolize chlorpyrifos to undergo either
oxidative desulfuration (Fig. 1), forming chlorpyrifos-oxon, or
dearylation (oxidative ester cleavage), forming 3,5,6-trichloro-2-
pyridinol
(TCPy)
and
diethylthiophosphate
(Kamataki
et
al.,
1976). Chlorpyrifos-oxon is a potent inhibitor of cholinesterases,
including acetylcholinesterase (AChE) and butyrylcholinesterase
(BuChE), by covalently binding to the active site of these enzymes
(Sultatos, 1994). Chlorpyrifos-oxon can be metabolized by hepatic
and extrahepatic A-esterases, such as paraoxonase-1 (PON1) (Pond
et al., 1998), and tissue B-esterases (e.g. carboxylesterase, CaE) to
form TCPy and diethylphosphate (Chanda et al., 1997). Formation
of TCPy (by either chlorpyrifos dearylation or chlorpyrifos-oxon
hydrolysis) is generally considered to be a detoxiﬁcation pathway,
and TCPy can be further metabolized by phase II enzymes to form
various conjugates (Bakke et al., 1976; Nolan et al., 1984). Conju-
gated and unconjugated TCPy, diethylphosphate, and diethylthiol-
phosphate are excreted in urine (Bakke et al., 1976; Nolan et al.,
1984).
Results from studies have suggested increased susceptibility in
young animals compared to adults from acute chlorpyrifos expo-
sures, the degree of which is variable with age, dose, and target tis-
sue (Marty et al., 2012; Pope et al., 1991; Timchalk et al., 2006;
Vidair, 2004; Whitney et al., 1995; Zheng et al., 2000). In one study,
age-dependent sensitivity to cholinesterase inhibition of varying
http://dx.doi.org/10.1016/j.yrtph.2013.10.005
0273-2300/ 2013 Elsevier Inc. All rights reserved.
⇑Corresponding author. Address: PO Box 999, Richland, WA 99354, USA. Fax: +1
(509) 376 9064.
E-mail address: jordan.smith@pnnl.gov (J.N. Smith).
Regulatory Toxicology and Pharmacology 69 (2014) 580–597
Contents lists available at ScienceDirect
Regulatory Toxicology and Pharmacology
journal homepage: www.elsevier.com/locate/yrtph

---CHUNK_BREAK---

69 (2014) 580–597 Contents lists available at ScienceDirect Regulatory Toxicology and Pharmacology journal homepage: www.elsevier.com/locate/yrtph degrees were demonstrated in plasma, red blood cells, and brain of
postnatal day (PND) 5, 12, and 17 rats dosed with 1 and 10 mg/kg
chlorpyrifos orally, where PND 5 animals appeared to be more sen-
sitive than adults at both doses, but PND 12 rats were only more
sensitive at the higher dose (Timchalk et al., 2006). In agreement
with those results, PND 12 rats had increased red blood cell cholin-
esterase inhibition compared to adults (2 mg/kg chlorpyrifos,
orally), but demonstrated similar plasma cholinesterase activities
and equivalent no adverse effect levels (NOEL; 0.5 mg/kg), indicat-
ing negligible age-dependent effects at lower doses for those age
groups (Marty et al., 2012). A benchmark dose analysis (BMD) on
that study (Marty et al., 2012) and meta-analysis of other studies
recommends equivalent BMD10 values for both children and adults
after single acute (1.7 mg/kg/day) and repeated (0.67 mg/kg/day)
doses (Reiss et al., 2012).
Several age-related factors could contribute to age-dependent
susceptibility including levels of metabolism and variable growth
rates
of
organs.
Age-related
increases
in
both
desulfuration and dearylation pathways on a liver mass basis
(Atterberry et al., 1997), and age-dependent changes in chlorpyri-
fos-oxon hydrolysis (Karanth and Pope, 2000) have all been
reported in rats. In humans, hepatic chlorpyrifos desulfuration,
chlorpyrifos dearlyation, and chlorpyrifos-oxon hydrolysis have
not demonstrated any age-dependent relationships on a micro-
somal protein basis; however, when scaling those values based
on liver volume, age-dependent differences existed (Smith et al.,
2011). Chlorpyrifos-oxon hydrolysis in plasma demonstrated an
age-dependent increase on a volume of plasma basis in humans,
with mean chlorpyrifos-oxon metabolism increasing over 3.5
times from <6 months in age to adulthood (Smith et al., 2011).
Differing rates of organ growth can also affect distribution of
chemicals. For example, relative fat levels in children are lower
than in adults, and conversely, relative brain size is higher in chil-
dren than in adults. Since approximately 11% of brain tissue is
lipid compounds (Poulin and Krishnan, 1995), high brain to fat
tissue ratios (as found in children) could augment partitioning
of lipophilic chemical compounds to brains of children compared
to that of adults.
Physiologically based pharmacokinetic and pharmacodynamic
(PBPK/PD) models provide a computational framework to quanti-
tatively incorporate age-dependent changes in physiology and
mechanisms of chemical disposition to predict net effects on target
tissue dosimetry and biological response. Several models have
been developed to assess age-dependent risk including caffeine
(Ginsberg et al., 2004), theophylline (Ginsberg et al., 2004), per-
chlorate (Clewell et al., 2007), bisphenol A (Willhite et al., 2008),
and chloroform (Liao et al., 2007). PBPK/PD models have been
developed for chlorpyrifos including models for ‘typical’ rats and
humans (Timchalk et al., 2002), chemical mixtures (Timchalk and
Poet, 2008), gestational exposure (Lowe et al., 2009), and age-
dependency in rats (Timchalk et al., 2007b). Hinderliter et al.,
(2011) developed estimates of response for two speciﬁc age groups
(3 and 30 years) linked to dietary exposure, and Foxenberg et al.,
(2011) made predictions of two age groups (1 and 19 years)
exposed to two organophosphates (parathion and chlorpyrifos)
based on extrapolating cytochrome P450-speciﬁc activities; how-
ever, a general age-dependent of chlorpyrifos in humans has not
been developed.
Cl
Cl
Cl
O
H
N
R
Cl
Cl
Cl
O
N
Phosphooxythiiran Intermediate
Trichloropyridinol (TCPy)
Chlorpyrifos Oxon
Diethylphosphate (DEP)
Diethylthiophosphate (DETP)
Trichloropyridinol Conjugate
Cytochrome P450
A & B-Esterases
S
O
Cl
Cl
Cl
C
H3
C
H3
P
O
O
O
N
Chlorpyrifos (CPF)
O
Cl
Cl
Cl
C
H3
C
H3
P
O
O
O
N
O
C
H3
C
H3
P
O
O
OH
S
C
H3
C
H3
P
O
O
OH
S
Cl
Cl
Cl
C
H3
C
H3
P
O
O
O
N
Cholinesterase Inhibition
Desulfuration
Dearylation
Fig. 1. Enzymatic metabolism of chlorpyrifos (CPF), chlorpyrifos-oxon (CPF-oxon), and 3,5,6-trichloro-2-pyridinol (TCPy).

---CHUNK_BREAK---

Inhibition Desulfuration Dearylation Fig. 1. Enzymatic metabolism of chlorpyrifos (CPF), chlorpyrifos-oxon (CPF-oxon), and 3,5,6-trichloro-2-pyridinol (TCPy). The purpose of this study was to quantitatively integrate age-
dependent parameters of physiology as well as chlorpyrifos phar-
macokinetics and pharmacodynamics into a life-stage model for
humans. Mathematical descriptions of age-dependent changes in
body weight, organ volumes, and metabolism from the literature
and experimental studies were incorporated into the model which
was tested against controlled adult human chlorpyrifos exposure
studies. This model will be useful for predicting chlorpyrifos dispo-
sition and biological response across life-stages.
2. Materials and methods
2.1. Chemicals and samples
Chlorpyrifos-oxon was kindly provided by the Dow Chemical
Company (Midland, MI, USA). Mixed human plasma was obtained
from Bioreclamation, Inc. (Liverpool, NY, USA). Other general labo-
ratory chemicals were purchased from Sigma–Aldrich (St. Louis,
MO, USA) and were reagent grade or better.
2.2. Human chlorpyrifos pharmacokinetic studies
There are two controlled human chlorpyrifos exposure studies
available for model development that have been evaluated for both
scientiﬁc and ethical considerations by the US Environmental Pro-
tection Agency Human Studies Review Board. In the ﬁrst study,
human volunteers were administered 0.5 mg/kg chlorpyrifos orally
by applying chlorpyrifos (in solvent that was subsequently evapo-
rated off) to the surface of a lactose tablet (Nolan et al., 1984). End-
points measured included TCPy levels in blood and urine as well as
chlorpyrifos levels in blood and plasma cholinesterase activity. In
the second study, volunteers were administered 0.5, 1, or 2 mg/
kg chlorpyrifos (neat) orally in a capsule (Kisicki et al., 1999;
Timchalk et al., 2002). Measured endpoints were chlorpyrifos lev-
els in blood, TCPy levels in blood and urine, and cholinesterase
activity in red blood cells.
2.3. Model structure
A life-stage PBPK/PD model was developed to describe the
absorption, distribution, metabolism, distribution, and excretion
of CPF. The PBPK/PD model structure was based on the original
model developed for diisopropylﬂuorophosphate (DFP) (Gearhart
et al., 1990), which has subsequently been adapted for chlorpyrifos
(Timchalk et al., 2002) and further modiﬁed for age-dependent
changes in rats (Timchalk et al., 2007b) (Fig. 2). The model
describes the time-course disposition of chlorpyrifos, chlorpyri-
fos-oxon, and TCPy as well as inhibition of several B-esterases by
chlorpyrifos-oxon including acetylcholinesterase, butyrylcholin-
esterase, and carboxylesterase.
Body weight and compartmental volumes for the life-stage
PBPK/PD model were scaled using an approach proposed by
Luecke et al. (2007) and Young et al. (2009). Using this approach,
body weight was scaled by age using a modiﬁed Gompertz growth
function (Eq. 1A for t0 to t2 and 1B for t2 to 1) that can be param-
eterized by gender or species, where body weight (BWT [kg]), and
Wx, ax, Rx, and bx are parameters that vary in steps by time denoted
as tx. These generalized equations were ﬂexible enough to describe
growth in a number of genders and species (for extrapolation) and
speciﬁc enough to describe growth phenomena such as adoles-
cence growth spurts (Luecke et al., 2007).
BWTðtÞtx:txþ1 ¼ Wx  e
Rx
eaxð1eaxtÞ þ bxðt  txÞ
ð1AÞ
BWTðtÞtx:txþ1 ¼ Wx  e
Rx
eaxð1eaxðttxÞÞ þ bxðt  txÞ
ð1BÞ
The same compartments were used in the life-stage model that
were used in the original PBPK/PD model (Timchalk et al., 2002)
and included brain, blood, diaphragm, fat, liver, rapidly perfused,
and slowly perfused compartments. The rapidly perfused compart-
ment consisted of a summation of kidney, spleen, lung, gastroin-
testinal
tract
(GI),
and
pancreas
volumes;
and
the
slowly
perfused compartment consisted of a summation of muscle, skin,
bone marrow, and non-fat adipose tissue volumes.
The life-stage PBPK/PD model incorporated both adipose and
lipid compartments descriptions in the model. Adipose tissue is
deﬁned as all tissue associated with adipose tissue (connective
and lipid tissue), while the fat compartment is lipid content only.
The non-fat adipose tissue (connective tissue, adipose compart-
ment subtract the fat compartment) was included in the slow com-
partment. This helps to balance out the total volume of distribution
and more accurately represent actual lipid levels in relation to adi-
pose
levels.
The
International
Commission
on
Radiological
Protection (ICRP) Publication 89 (2002) describes adipose tissue
as a combination of fat and connective tissue, and reference fat
content of adipose tissue is 40% at birth and increases to 80% in
adults. Thus it was important to account for these differences, as
failure to do so could lead to age-related inaccurate compartment
volume estimates for fat or fat partition coefﬁcients (if one
assumes a constant lipid content of adipose tissue). These potential
inaccuracies could have substantial implication on overall pharma-
cokinetics for lipophilic compounds like chlorpyrifos.
Compartmental volumes (on a fractional body weight basis (VC)
for X compartment) were scaled with polynomial equations of var-
ious orders (n) as a function of body weight (BWT [g]), where An is
the coefﬁcient for each expression of the polynomial (Eq. 2). This
framework could be used to deﬁne and switch among compart-
ments of various species and genders with ease using one standard
model.
VCx ¼ An  BWTn þ An1  BWTn1 þ    þ A2  BWT2
þ A1  BWT þ A0
ð2Þ
Oral absorption of chlorpyrifos is described by a two-compart-
ment empirical model representing a stomach linked to an
external intestinal compartment, which is linked to the liver
compartment. Movement of chlorpyrifos among these absorption
compartments are all described as ﬁrst-order transfer rates includ-
ing from stomach (Stom) to intestine (Int) (ksi) and intestine to
liver (kai) (Eqs. (3) and (4)). This two-compartment is required to
accurately describe chlorpyrifos absorption kinetics (Timchalk
et al., 2002).
dAStom
dt
¼ ksi  AStom
ð3Þ
dAInt
dt
¼ ksi  AStom  kai  AInt
ð4Þ
Once absorbed, chlorpyrifos and chlorpyrifos-oxon were dis-
tributed among tissue compartments mediated by blood circula-
tion
described
as
a
ﬂow-limited
process
previously
published mathematical descriptions (Timchalk et al., 2002). The
fraction of the compound not bound to plasma proteins (simply
described mathematically as a fraction, Timchalk et al., 2002)
was free to partition to various compartments described by parti-
tion coefﬁcients.
Metabolism of chlorpyrifos and chlorpyrifos-oxon was imple-
mented using in vitro to in vivo approach, in which metabolism,
measured in vitro, was extrapolated to in vivo values using micro-
somal concentration and compartmental volume to scale metabo-
lism (Lipscomb and Poet, 2008). Chlorpyrifos metabolism by
cytochrome P450-mediated processes in the intestine, liver, and

---CHUNK_BREAK---

(Lipscomb and Poet, 2008). Chlorpyrifos metabolism by cytochrome P450-mediated processes in the intestine, liver, and brain were described using Michaelis–Menten kinetics. Chlorpyri-
fos-oxon metabolism by PON1 was also described using Michaelis–
Menten kinetics in those same compartments as chlorpyrifos
(except brain) as well as in plasma.
B-esterase metabolism and inhibition were described in the
liver, plasma, red blood cells (RBC), brain, and diaphragm as sec-
ond-order processes. Tissue B-esterase enzyme levels and binding
sites were calculated from enzyme turnover rates and enzyme
activity levels and were balanced based on degradation, synthesis,
and inhibition rates. Inhibition of B-esterase was calculated as
described in previous models (Timchalk et al., 2002) using stoichi-
ometric inhibition by chlorpyrifos-oxon concentration (based on
an apparent bimolecular inhibition constant), reactivation of inhib-
ited enzyme, aging of inhibited enzyme, and degradation/synthesis
of new enzyme.
In order to describe changes in anatomy during growth, the life-
stage PBPK/PD model dynamically changes during a simulation of
the individual over its life span changing body weight, compart-
mental volumes, and all values scaled to those components. To
accommodate the new description of dynamic compartment vol-
umes, the mathematical description of percent inhibition also
had to be altered from the original description (Timchalk et al.,
2002). In the original chlorpyrifos PBPK/PD model, amount of unin-
hibited enzyme was divided by the total number of binding sites to
calculate percent esterase activity (Timchalk et al., 2002). In the
life-stage model, a naïve level of uninhibited enzyme is calculated
based on the total number of binding sites changing over time by
only degradation and synthesis of new enzyme (Kd; Eqs. (5) and
(6)). The ratio of the uninhibited enzyme, as calculated by
Timchalk et al. (2002), to these naïve levels result in the calculation
of percent esterase activity, which remains at a constant 100% in a
naïve (i.e. unexposed) simulation.
dAChENaive
dt
¼ Ks  AChENaive  Kd
ð5Þ
%Activity ¼
AChENaive
 100
ð6Þ
TCPy pharmacokinetics was described as a one-compartment
model (Timchalk et al., 2002). All available data for human TCPy
levels in urine were measured following acid hydrolysis of TCPy
conjugates (Kisicki et al., 1999; Nolan et al., 1984; Timchalk
et al., 2002), thus chlorpyrifos elimination was assumed to be com-
pletely facilitated as urinary TCPy.
2.4. Model parameters
Model parameters consisted of physiological values, partition
coefﬁcients, and biochemical values that were previously pub-
lished, experimentally derived, or optimized computationally.
Parameters of the Gompertz body weight function (Table 1) and
polynomial descriptions of compartment volumes (Table 2) were
obtained from previously published sources (Luecke et al., 2007;
Young et al., 2009). The model developed here (which is designed
for a ‘‘typical’’ person) is being used in an allied study to assess
implications of model uncertainty and inter-individual variation
in a risk assessment context (Poet et al., 2013). There is a signiﬁ-
cant portion of our population that have body weights higher than
what could be used to reliably used to predict organ volumes with
previous methods. Thus an effort was made to extend organ
Chlorpyrifos
Qc
Venous Blood 
Arterial Blood 
Qs
Qr
Qd
Qb
Cvb 
Ql
Cvs 
Cvr 
Cvd 
Cvl 
Qf
Cvf 
KsI 
KaI 
Oral Exposure 
Fa
Slowly Perfused 
Fat 
Rapid Perfused 
Stomach 
Intestine 
 PON1 
CYP450 
Urinary 
Clearance 
Volume of 
Distribution 
CPF-Oxon
Cvo 
Cao 
Qs
Qr
Qd
Qb
Cvbo 
Ql
Cvso 
Cvro 
Cvdo 
Cvlo 
Cvfo 
Slowly Perfused 
Fat 
Rapid Perfused 
Qf
Synthesis of New Esterase 
“Free”
CPF-Oxon +
Degradation of Esterase 
Released TCPy Metabolite 
(TCPy model) 
Regeneration 
B-Esterase (B-EST) Inhibition 
(shaded compartments) 
Inhibition 
µm hr-1
Free Esterase 
Aged Complex 
Oxon Esterase 
µmole hr-1
Fig. 2. The life-stage physiologically based pharmacokinetic and pharmacodynamic (PBPK/PD) model structure used to describe the disposition of chlorpyrifos (CPF),
chlorpyrifos-oxon (CPF-oxon), and 3,5,6-trichloro-2-pyridinol (TCPy). The model also describes inhibition of B-esterases by chlorpyrifos-oxon in compartments shaded gray.

---CHUNK_BREAK---

3,5,6-trichloro-2-pyridinol (TCPy). The model also describes inhibition of B-esterases by chlorpyrifos-oxon in compartments shaded gray. volume polynomial ﬁts to larger body weights (170 kg), including
fat (both male and female), adipose, brain, liver, and muscle. Previ-
ously published polynomials or constants were used to deﬁne all
other compartmental volumes (Table 2). The polynomial ﬁtting
procedure used here for reﬁts was similar to that used previously
with some minor modiﬁcations (Luecke et al., 2007; Young et al.,
2009). Polynomial models of orders 1–6 were ﬁt to available data,
and then the best ﬁt model was chosen based on the model with
the lowest Bayesian information criterion (BIC). For data, emphasis
was placed on reference values for various compartments as
deﬁned by the ICRP Publication 89 (2002), which presents detailed
information on age- and gender-related differences in anatomical
and physiological characteristics of reference individuals. This
emphasis was placed especially for body weights from birth to
70 kg, while other references were used for compartment volume
data at larger body weights. Besides the ICRP Publication 89 (2002),
Luecke et al. (2007) and Young et al. (2009), two other references
were utilized for compartmental reﬁts. First, a study aimed at eval-
uating differences in body mass and composition in respect to
muscle strength and output between obese and normal weighted
individuals, was used for fat and adipose tissue reﬁts (Lafortuna
et al., 2005). A study measuring skeletal muscle mass and distribu-
tion men and women with magnetic resonance imaging was used
for muscle reﬁts (Janssen et al., 2000). Data for some compart-
ments were not available up to the desired 170 kg. For those
compartments, extrapolations were made with published relation-
ships extrapolating data points for body weights of 150–175 kg at
5 kg intervals.
Other
parameters
determining
included
transfer rates and partition coefﬁcients (Table 3). Fraction of dose
absorbed was determined from a non-compartmental pharmacoki-
netic analysis of human urinary excretion rate data based on the
assumption that all chlorpyrifos is eliminated as TCPy in urine
(Nolan et al., 1984). The total molar amount of TCPy eliminated
was divided by the ratio of the area under the curve (AUC) from
0 to the time of the last data point to the AUC from 0 to 1 resulting
in the amount absorbed. The elimination constant for TCPy (ke)
was calculated from a non-compartmental pharmacokinetic analy-
sis of TCPy levels in human blood (Nolan et al., 1984). The volume
of distribution for TCPy was calculated utilizing partitioning coef-
ﬁcients
predicted
an
algorithm
(Schmitt,
2008).
This
approach calculates partitioning coefﬁcients based upon the com-
position of tissues in terms of water, various types of lipid content,
phsopholipid content, proteins, and pH differences using chemical
compound speciﬁc lipophilicity, pKa, and plasma protein-binding
(Schmitt, 2008; Smith et al., 2010). Tissue-speciﬁc partitioning
coefﬁcients were scaled to the appropriate compartment volume
over various body weights. The volume of distribution was calcu-
lated as the total amount of TCPy in all compartments divided by
the TCPy concentration in blood. To ease coding of this volume of
distribution in the model, an allometric equation was ﬁt to the pre-
dicted volume of distributions over various body weights (Eq. 7),
where A and B are allometric constants.
VDTCPy ¼ A  BWTB
ð7Þ
The transfer rate of chlorpyrifos from stomach to intestine,
absorption rate from intestine to liver of chlorpyrifos, were opti-
mized in tandem using TCPy levels in blood and plasma cholines-
terase inhibition (Nolan et al., 1984). Due to differences in dose
formulations, model simulations of the two human studies used
different absorption parameters. For the Kisicki study, the stomach
to intestine transfer rate was optimized independently using levels
of TCPy in blood (Kisicki et al., 1999; Timchalk et al., 2002). Trans-
fer rate of chlorpyrifos-oxon and TCPy from intestine to liver was
optimized in a rat model using rats dosed with TCPy (Busby-
Hjerpe et al., 2010; Marty et al., 2012; Timchalk et al., 2007a;
Timchalk et al., 2002). Blood ﬂows to each compartment were
scaled as a constant ﬂow per compartmental volume, and total car-
diac output was a summation of all blood ﬂows to all compart-
ments. Fractional binding of chlorpyrifos to serum albumin was
measured previously using a dialysis system (Lowe et al., 2009).
As chlorpyrifos-oxon undergoes rapid hydrolysis in the presence
of albumin, it was assumed that chlorpyrifos and chlorpyrifos-oxon
have equivalent fraction binding in plasma. Partition coefﬁcients
were measured previously using plasma and vegetable oil and
extrapolated to tissues using a QSAR approach (Lowe et al., 2009).
Table 1
Parameter values for a Gompertz growth function used to describe body weight as a
function of age in the life-stage model (Luecke et al., 2007).
Female
Male
t0

t1
2.9490
2.9490
t2

t3
21.8653
21.6602
b0, b2

b1
2.6727
2.4624
b3
0.3113
-0.0911
W0, W1
3.4
3.4283
W2, W3
34.8806
34.3545
R0, R1
2.0740
2.1882
R2, R3
0.2128
0.1798
a0, a1
1.5046
1.5063
a2, a3
0.4438
0.2212
Table 2
Parameter values for polynomial functions describing compartment volume (fraction of body weight) as a function of body weight (g) used in the life-stage model.
Compartment
A0
A1
A2
A3
A4
A5
A6
1.216  101
3.465  106
4.354  1011
2.463  1016
5.132  1022
Hepatic
3.939  102
7.058  107
1.155  1011
8.016  1017
1.869  1022
8.970  102
3.500  107
6.540  1013
Fat-male
3.484  102
2.803  105
1.422  109
2.892  1014
2.718  1019
1.203  1024
2.036  1030
Fat-female
9.217  102
1.401  105
6.787  1010
1.540  1014
1.558  1019
7.249  1025
1.274  1030
Adipose
2.044  101
2.617  105
1.542  109
3.268  1014
3.116  1019
1.387  1024
2.35  1030
Lung
1.860  102
4.550  108
Kidney
7.260  103
6.690  108
3.330  1013
Spleen
3.120  103
5.570  109
GI
1.650  102
Muscle
1.251  101
1.458  105
2.927  1010
2.114  1015
5.250  1021
Skin
1.030  101
2.560  106
3.680  1011
2.580  1016
8.620  1022
1.100  1027
Bone marrow
2.100  102
3.000  104
Brown et al. (1997) and
Luecke et al. (2007)
Pancreas
1.480  103
Young et al. (2009) and

Metabolic parameters were ﬁt or acquired from several sources
(Table 3). Hepatic chlorpyrifos and chlorpyrifos-oxon metabolism
were measured previously in human microsomes from donors of
a wide age range (13 d–75 yr) and demonstrated a consistent level
of metabolism across ages (Smith et al., 2011). Chlorpyrifos-oxon
metabolism in plasma was also measured in humans (3 d–43 yr),
and Vmax values demonstrated an age-dependent increase (Smith
et al., 2011). Thus Vmax was scaled using a logistic model as a func-
tion of age (Eq. 8), where A, B, and C are parameters. Hepatic in vitro
Vmax values were scaled using a constant microsomal protein level
across all ages (33 mg/g tissue) (Wilson et al., 2003), and in vitro Km
values were scaled based upon predictions of unbound substrate in
the in vitro system to that of the in vivo system (39% of measured
Km) (Poulin and Haddad 2011; Poulin et al., 2011). In order to
determine the relative contribution of chlorpyrifos-oxon hydroly-
sis by A- and B-esterases, samples of human plasma (200 lL) were
spiked with chlorpyrifos-oxon ranging from 0.1 nm to 10 lM,
including a control (0 nM). After 120 min, cholinesterase activity
Table 3
Values for parameters describing the disposition of chlorpyrifos (CPF), chlorpyrifos-oxon (CPF-oxon), and 3,5,6-trichloro-2-pyridinol (TCPy) in the life-stage model.
Value
Blood ﬂow (L/h/kg tissue)
30.6
Price et al. (2003)
50.4
Price et al. (2003)
Fat
1.45
Luecke et al. (2007), Cowles et al. (1971) and Price et al. (2003)
61.8
Adrenal/Spleen mean: Price et al. (2003)
1.8
Bone marrow: Price et al. (2003)
85.2
Luecke et al. (2007)
Partition coefﬁcients (tissue:blood)
CPF
16.5
12.8
Fat

16.5
Lowe et al. (2009
5.6
4.5
Fat

5.6
1.8
1.8
Hepatic dearylation

Hepatic desulfuration

---CHUNK_BREAK---

16.5 Lowe et al. (2009 5.6 4.5 Fat 5.6 1.8 1.8 Hepatic dearylation Hepatic desulfuration Hepatic CPF-oxon hydrolysis
1.29  105

Blood CPF-oxon hydrolysis
Logistic Fit (see text)
Smith et al. (2010)

Smith et al. (2010)
Intestinal dearylation

Intestinal CPF-oxon hydrolysis

Intestinal desulfuration

Brain dearylation
Extrapolated (see text)

Brain desulfuration
0.91
Extrapolated (see text)
Measured in liver Smith et al. (2010)
Transfer rates (/h)
CPF stomach to intestine
0.31/0.086
Fit to Nolan et al. (1984)/Kisicki et al. (1999)
Intestinal absorption to liver
CPF
3.1
Fit to Nolan et al. (1984)
3.9
Fit to rat data Marty et al. (2012)
8.5
Fit to rat data Timchalk et al. (2007a) and Busby-Hjerpe et al. (2010)
Plasma protein binding (%)
CPF

Oxon

TCPy compartmental model
Ke (/h)
0.024
Nolan et al. (1984)
Volume of distribution constant A
0.176
Fit to Schmitt et al. (2008)
Volume of distribution constant B
1.01
Fit to Schmitt et al. (2008)

was measured using the Ellman assay (Ellman et al., 1961). Intes-
tinal metabolism of chlorpyrifos and chlorpyrifos-oxon was mea-
sured in rat enterocytes (Poet et al., 2003), and Vmax values were
extrapolated to humans. Km values were assumed to be equivalent
to the Km values measured in liver from humans (Smith et al.,
2011). Chlorpyrifos metabolism in brain was estimated based on
an extrapolation from limited studies in vitro with rat tissue
(Timchalk et al., 2012). Chlorpyrifos dearylation in brain micro-
somes was 115-fold lower than in hepatic microsomes. Formation
of chlorpyrifos-oxon in brain microsomes was below the limit of
detection (30 ng/mL). Thus chlorpyrifos metabolism in brain was
estimated at 115 times lower than hepatic chlorpyrifos metabo-
lism (for both desulfuration and dearylation) on a microsomal pro-
tein basis.
Vmax ¼
A
1 þ e
Bage
C
ð8Þ
Pharmacodynamic parameters were acquired from a variety of
literature sources and included cholinesterase activities, enzyme
aging, degradation, reactivation, and turnover rates (Table 4)
(Albers et al., 2010; Hojring and Svensmark, 1976; Li et al., 2005;
Maxwell et al., 1987; Mortensen et al., 1998b; Pope et al., 2005;
Sidell and Kaminskis, 1975). Veriﬁcation of the bimolecular inhibi-
tion rate constants was achieved by directly determining the ace-
tylcholinesterase and butyrylcholinesterase inhibition dynamics
in rat plasma, brain, and saliva (Kousba et al., 2007; Kousba
et al., 2004).
2.5. Sensitivity analysis
A local sensitivity analysis was conducted to identify the most
important parameters for estimating acetylcholinesterase inhibi-
tion in red blood cells and brain from an oral dose of 3 lg/kg chlor-
pyrifos (the reference dose) in 0.5 and 30 yr humans. In order to
conduct the analysis, age-dependent parameters deﬁned as equa-
tions were replaced with discrete constants. All variables in the
model were subjected to the sensitivity analysis. Normalized sen-
sitivity coefﬁcients were calculated for a 1% change in a given
model parameter when all other parameters were held ﬁxed. A
more rigorous sensitivity analysis will be implemented in future
work to gauge the implications of parameter uncertainty and
inter-variability (Poet et al., 2013).
2.6. Statistics and model coding
The PBPK/PD model was coded in acslXtreme 3.0.2.1 (Aegis
Technology, Huntsville, AL USA) and included ordinary differential
equations and algebraic functions. Optimizations of PBPK/PD
model parameters were also conducted using acslXtreme using
the Nelder-Mead or Quasi-Newton (if less than two variables being
optimized) algorithms. The heteroscedasticity was set to 1.0,
except for TCPy levels in blood, which was set to 0.5, because initial
ﬁts with a heteroscedasticity factor of 1.0 did not ﬁt early time
points well visually. Initial values were set by adjusting parameters
visually, then allowing the optimization to occur bounded by rea-
sonable values. R: A language and environment for statistical com-
puting, version 2.9.0, 2.11.1, or 2.13.1 (R Foundation for Statistical
Table 4
Values for parameters describing B-esterase activity and inhibition thereof by chlorpyrifos-oxon (CPF-oxon) in the life-stage model.
Value
Enzyme activity (lmol/kg/h)
4.4  105
NA
1.02  104
4.27  105
Albers et al. (2009)
7.74  104
BuChE
4.68  104
2.63  105
Sidell and Kaminskis (1975)
3.0  104
2.64  104
2.88  105
Hojring et al. (1976)
NA
Li et al. (2005)
1.27  106
Pope et al. (2005)
3.18  105
Degradation rates (/h)
Timchalk et al. (2002) and Gearhart et al. (1990)
BuChE
0.0024
Fit to Nolan et al. (1984)
7.54  104
Enzyme reactivation rate (/h)
0.014
Carr and Chambers (1996) and Timchalk et al. (2002)
0.0014
Carboxyl
0.014
Enzyme Aging Rate (/h)
0.0113
Enzyme turnover rate (/h)
1.17  107
3.66  106
Carboxyl
1.086  105
Bimolecular inhibition rate (lM/h)

Kousba et al. (2004) and Kousba et al. (2007)

---CHUNK_BREAK---

 105 Bimolecular inhibition rate (lM/h) Kousba et al. (2004) and Kousba et al. (2007) Computing, Vienna, Austria) was used to analyze data, calculate
AUC values, and ﬁt various functions including polynomial descrip-
tions of compartments, logistic function for chlorpyrifos-oxon
hydrolysis Vmax, and two-compartment pharmacokinetic models.
For summary statistics, geometric means are reported with 90%
conﬁdence intervals in parentheses.
3. Results
3.1. Parameterization-compartment volumes
The parameterized Gompertz function for body weights of
males and females (Luecke et al., 2007) provided good predictions
of 2007–2008 US population body weight from the National Health
and
Nutrition
Examination
Survey
(NHANES)
(Supplemental
Fig. 1).
Most literature compartment ﬁts accurately described age-
dependent growth for body weights up to 170 kg; however due
to the unpredictable nature of polynomials outside of the range
of ﬁtted data, fat (both male and female), adipose, brain, liver,
and muscle compartments were all reﬁtted for extrapolations of
body weights up to 170 kg (Fig. 3, Table 2). Raw data and extrap-
olations of data (150–175 kg body weights) were used to ﬁt male
and female fat compartments (Supplemental Figs. 2A and B)
(2002; Lafortuna et al., 2005). Data from these same sources were
used for adipose tissue, based on the assumption that 80% of adi-
pose tissue in adults is fat, as did ICRP Publication 89 in their der-
ivation of reference adipose levels for adults (2002). Resulting ﬁts
were 6th order polynomials for male fat and adipose compart-
ments and a 6th order polynomial was ﬁt for the female fat com-
partment (even though it did not have the lowest BIC) to
maintain consistency with males. Source data for the brain com-
partment was acquired for body weights less than (2002) and
greater than 70 kg (Young et al., 2009). Extrapolations of brain vol-
ume were made for using 150–175 kg body weights using a table
provided by Young et al., (2009). The resulting ﬁt was a 4th order
polynomial equation (Supplemental Fig. 3A). The liver compart-
ment was reﬁtted using reference values for liver volumes as well
as extrapolated for 150–175 kg body weights as previously for
brain volume (Supplemental Fig. 3B) (2002; Young et al., 2009).
Originally, all data were used in ﬁtting attempts (Young et al.,
2009), but those efforts were problematic. Those ﬁts resulted in
polynomial equations that attempted to explain variability in liver
weights, and thus a smooth function across body weights was
unattainable. Reference values for liver volumes resulted in a 4th
order polynomial that was a much smoother ﬁt. Raw muscle data
(2002; Janssen et al., 2000) and extrapolations of body weights
150–170 kg based on the equation presented in Janssen et al.
(2000) were used to ﬁt a 4th order equation that is summed into
the slow compartment (Supplemental Fig. 3C). These compartment
ﬁts in addition to the other compartments from various sources
provide a total volume of distribution that is 75–95% of body
weight depending on age (Supplemental Fig. 4).
The TCPy volume of distribution was predicted over various
body weights using a partitioning algorithm (Schmitt, 2008). Parti-
tioning of TCPy to each compartment in the PBPK model was pre-
dicted and the amount of TCPy in each compartment was
calculated using compartmental volumes for various body weights
3–170 kg
calculated
polynomial
scaling
as
previously
described. For each body weight, the ratio of total TCPy in all com-
partments to the TCPy concentration in blood was used to calculate
the TCPy volume of distribution (Supplemental Fig. 5). An allome-
tric equation was ﬁt to these predictions for easier coding into the
PBPK model (Eq. 7, A: 0.176, B: 1.01) (Table 3).
3.2. Parameterization-other parameters
Since blood ﬂows were scaled as constant ﬂow per compart-
ment volume, they demonstrated similar ontogeny patterns as
compartment volumes (Fig. 4). In 30 yr old adults, highest overall
blood ﬂows were to the rapidly perfused compartment; while in
neonates, the highest blood ﬂow was to the brain.
Previously measured chlorpyrifos-oxon hydrolysis Vmax values
demonstrated an age-dependent increase in plasma (Smith et al.,
2011), and a logistic model (Eq. 8) was ﬁt to the data with param-
eter values of 4.32  105, 3.052, and 3.90 for the logistic parame-
ters
A,
B,
and
C,
respectively
(Supplemental
Fig.
6).
This
mathematical description describes age-dependent description of
Vmax values over the ontogeny of this enzymatic system. Since both
A- and B-esterases are present in plasma, cholinesterase inhibition
was measured in undiluted human plasma after incubation with
chlorpyrifos-oxon to determine the relative contribution of each
esterase to chlorpyrifos-oxon hydrolysis. After 2 h, 10 nM of chlor-
pyrifos-oxon inhibited plasma cholinesterase activity by 10%, and
nearly all cholinesterase activity was inhibited with 500 nM chlor-
pyrifos-oxon (Supplemental Fig. 7). This indicates that the relative
contribution of chlorpyrifos-oxon hydrolysis by B-esterases was
negligible compared to A-esterases at concentrations used to

0.1

Fat
A
Tissue Volume (L)

0.1

Rapid
Slow
B
Tissue Volume (L)
Fig. 3. Compartment volumes as a function of body weight for males/gender neutral (solid lines) and females (dotted lines) of the life-stage model as calculated by
polynomial equations of fractional body weight (Luecke et al., 2007; Young et al., 2009). Symbols represent tissue volumes predicted for a typical 70 kg male using the original
chlorpyrifos PBPK/PD model (Brown et al., 1997; Timchalk et al., 2002). Arrows indicate body weights of typical humans at 6 months, 3 yr, and 30 yr old as determined by a
generalized Gompertz equation (Luecke et al., 2007). Note: y-axes are on a logarithmic scale.

---CHUNK_BREAK---

a generalized Gompertz equation (Luecke et al., 2007). Note: y-axes are on a logarithmic scale. measure the in vitro Michaelis–Menten metabolism kinetics in
diluted (1/200) human plasma (72.3–2400 lM) (Smith et al.,
2011).
Fraction of chlorpyrifos dose absorbed was determined in
humans using ratios of AUC values [AUCð0 to tlastÞ to AUC(0 to 1)] of
urinary excretion rates and total amount of TCPy eliminated. After
administration to chlorpyrifos on a lactose tablet, subjects demon-
strated a fractional absorption of 77% (Nolan et al., 1984), while
those that were administered neat chlorpyrifos in a capsule
absorbed 21% of the dose (Kisicki et al., 1999; Timchalk et al.,
2002).
Pharmacokinetic and cholinesterase inhibition data from Nolan
et al. (1984) was used to calibrate the PBPK/PD model. TCPy was
measured in all blood and urine samples. Chlorpyrifos in blood
was also measured very close to the limits of detection and dis-
played erratic temporal behavior. The chlorpyrifos transfer rate
from stomach to intestine (ksi, 0.31 h1) and the chlorpyrifos
absorption transfer rate from intestine to liver (kai, 3.1 h1) was
ﬁt using TCPy levels in blood and plasma cholinesterase inhibition
data. Since chlorpyrifos can be metabolized in the GI tract, ratios of
these parameters can alter the relative absorption of chlorpyrifos
and TCPy, with blood levels of chlorpyrifos being relatively sensi-
tive to ksi compared to kai. The degradation rate of butyrylcholin-
esterase was ﬁt to the plasma cholinesterase inhibition data
(Nolan et al., 1984).
Ultimately, simulations of oral chlorpyrifos doses resulted in
levels of TCPy in blood and urine that were in agreement with pre-
vious observed values. The peak geometric mean TCPy concentra-
tion (with 90% conﬁdence interval) in blood was 4.7 (3.4–6.4) lM
at 6 h post ingestion (Nolan et al., 1984). At the same dose and
time, the life-stage PBPK/PD model predicts a TCPy concentration
of 4.5 lM in blood of a 30 year old male and a slightly higher peak
level at 9.4 h (Fig. 5A). In urine, 70% of the total dose (83.3 (70.5–
98.6) lmol) was excreted by 120 h (Nolan et al., 1984), and the
model predicts 72% (85.5 lmol) for the same metric (Fig. 5B).
Life-stage PBPK/PD predictions of cholinesterase inhibition are
very similar to those measured previously in adult humans.
Nolan et al. (1984) measured peak inhibition of plasma cholines-
terase activity (geometric mean: 17 [13–21 90% conﬁdence inter-
vals]% control activity) at 24 h and no signiﬁcant changes to red
blood cell cholinesterase following an oral dose of 0.5 mg/kg chlor-
pyrifos. Substantial recovery of plasma cholinesterase (82 [68–
99]% control cholinesterase activity) occurred by 648 h. The life-
stage PBPK/PD model predicts 19% control plasma cholinesterase
activity at 24 h, and peak inhibition (17% control activity) at
13.7 h (Fig. 8A). The model also predicts 92% of control cholinester-
ase activity in red blood cells at peak inhibition (11.5 h, data not
shown). The life-stage model predicted cholinesterase activity to
recover at a similar rate as observed data, as the model predicts
84% control plasma cholinesterase activity at 648 h.
3.3. Validation in adult humans
A different study was used to validate the model for adults, in
which adult human volunteers were administered 0.5, 1, or
2 mg/kg chlorpyrifos in a capsule (Kisicki et al., 1999; Timchalk
et al., 2002). Due to a different formulation of chlorpyrifos from
the Nolan et al. (1984) study, the chlorpyrifos transfer rate from
stomach to small intestine was ﬁt to TCPy levels in blood of the
1 mg/kg dose group (Kisicki et al., 1999; Timchalk et al., 2002).

Fat
A
Blood Flow (L/h)

Rapid
Slow
B
Blood Flow (L/h)
Fig. 4. Blood ﬂow to various compartments as a function of body weight for males or both genders (solid lines) and females (dotted lines) of the life-stage model. Symbols
represent blood ﬂows for a typical 70 kg male using standard allometric approaches (Brown et al., 1997; Timchalk et al., 2002). Arrows indicate body weights of humans at
6 months, 3 yr, and 30 yr old as determined by a generalized Gompertz equation (Luecke et al., 2007). Note: y-axes are on a logarithmic scale.

0.1

A
TCPy in Plasma (µmol/L)

100 B
TCPy in Urine (µmol)

0.1

Fig. 5. Life-stage model predictions of 3,5,6-trichloro-2-pyridinol (TCPy) concentrations in plasma (A) and urine (B) from a human volunteer study (Nolan et al., 1984). Data
represent geometric means with 90% conﬁdence intervals for 5 individuals following an oral chlorpyrifos dose of 0.5 mg/kg (Nolan et al., 1984). Note: y-axis in (A) is on a
logarithmic scale.

The life-stage PBPK/PD model was used to simulate chlorpyrifos
and TCPy levels in plasma for several individuals using estimated
absorbed doses determined from total TCPy excreted in urine.
Chlorpyrifos levels were very near the limits of quantitation
(0.003 lM), and several individuals in the 1 and 2 mg/kg dose
group had quantiﬁable chlorpyrifos levels in blood. Using individ-
ualized fractions of absorption based on urinary TCPy elimination,
the model slightly over predicted chlorpyrifos levels in blood+
(Fig. 6).
For summarized data sets, geometric mean (with 90% conﬁ-
dence intervals) peak TCPy concentrations in blood (8 h) were 0.8
(0.6–1.0), 1.5 (1.2–2.0), and 2.6 (1.9–3.2) lM, respectively for three
dose groups (Kisicki et al., 1999; Timchalk et al., 2002). Using a
fractional absorption of 0.21, the life-stage model predicts 0.7,
1.4, and 2.8 lM TCPy at that same time point (Fig. 7A), and urinary
excretion is similar to those predicted by the model (Fig. 7B). Red
blood
cell
cholinesterase
activity
displayed
no
signiﬁcant
inhibition (Kisicki et al., 1999; Timchalk et al., 2002). The life-stage
PBPK/PD model predicts 94% control cholinesterase activity at
peak inhibition (27 h), which is similar to what was measured
(Fig. 8B–D).
3.4. Life-stage predictions
The
life-stage
PBPK/PD
model
predicts
age-dependent
responses in pharmacokinetics and resulting cholinesterase inhibi-
tion in humans from chlorpyrifos exposure. PBPK/PD model simu-
lations of 6 months, 3 yr, and 30 yr old humans at various doses
(100% oral absorption) predict that adults will have the highest
peak chlorpyrifos levels in blood (Figs. 9A and 10A). At single high
oral doses P0.6 mg/kg, 6 months infants will have the highest
peak levels of chlorpyrifos-oxon in blood (e.g. 55% higher at
1 mg/kg chlorpyrifos), and below that, adults will have the highest
levels (Figs. 9B and 10B). Higher levels of chlorpyrifos-oxon result

0.1

10 A: 2 mg/kg
CPF
LOQ

0.1

D: 0.5 mg/kg
LOQ
CPF

0.1

C: 1 mg/kg
CPF
LOQ

0.1

B: 2 mg/kg
LOQ
CPF
Fig. 6. Life-stage model predictions of chlorpyrifos (CPF) and 3,5,6-trichloro-2-pyridinol (TCPy) concentrations in four individuals from a human volunteer study (Kisicki
et al., 1999; Timchalk et al., 2002). Individuals A and B were dosed with 2 mg/kg CPF (0.21 and 0.14 fractional absorption, respectively), individual C was dosed with 1 mg/kg
CPF (0.26 fractional absorption), and individual D was dosed with 0.5 mg/kg CPF (0.23 fractional absorption). The limit of quantitation (LOQ) is indicated as a dotted line. Note:
y-axis is on a logarithmic scale.

B
TCPy in Urine (µmol)

0.1

10 A
TCPy in Plasma (µmol/L)
Fig. 7. Life-stage model predictions of 3,5,6-trichloro-2-pyridinol (TCPy) concentrations in plasma (A) and urine (B) from a human volunteer study (Kisicki et al., 1999;
Timchalk et al., 2002). Data represent geometric means with 90% conﬁdence intervals for 12 individuals dosed with 0.5 (diamond), 1.0 (circle), or 2 mg/kg (triangle) CPF. Note:
y-axis in 7B is on a logarithmic scale.

---CHUNK_BREAK---

(circle), or 2 mg/kg (triangle) CPF. Note: y-axis in 7B is on a logarithmic scale. in higher amounts of peak red blood cell acetylcholinesterase (e.g.
13% more inhibition at 1 mg/kg chlorpyrifos) and plasma cholines-
terase activity inhibition in infants compared to adults at doses
P0.6 mg/kg chlorpyrifos (Figs. 9C, D and 10C). Plasma cholinester-
ase is inhibited at lower levels of chlorpyrifos-oxon than red blood
cell acetylcholinesterase, and after an oral dose of 0.6 mg/kg chlor-
pyrifos, 99% of plasma cholinesterase was predicted to be inhib-
ited in both adults and 6 months infants (Fig. 9D). Thus the model
predicts adults will have lower levels of plasma cholinesterase
activity compared to infants at equivalent doses through the
majority of the dynamic range of plasma cholinesterase inhibition.
In the brain, trends in peak chlorpyrifos concentrations are pre-
dicted to mirror those in blood, where adults have higher chlor-
pyrifos levels than 6 months olds (Fig. 11A). There are two
sources
of
in
the
brain,
formed from hepatic chlorpyrifos metabolism and chlorpyrifos-
oxon formed locally due to low levels chlorpyrifos metabolism in
the brain. Because of these two chlorpyrifos-oxon sources, higher
levels of chlorpyrifos-oxon will be formed in the brains of adults
compared to 6 months infants because of higher chlorpyrifos levels
(with the assumption of no age-dependent differences in brain
metabolism rates), and at doses P0.6 mg/kg chlorpyrifos, chlor-
pyrifos-oxon
formed
hepatically
will
be
slightly
greater
in
6 months infants than adults. Overall, the model predicts slightly
higher levels of chlorpyrifos-oxon in adults than in 6 months old
infants (e.g. 8% higher at 5 mg/kg chlorpyrifos), suggesting that
even low levels of localized chlorpyrifos metabolism may be
important (Fig. 11B). Due to stoichiometric cholinesterase inhibi-
tion, peak inhibition levels of brain acetylcholinesterase activity
follow the same pattern as that of peak chlorpyrifos-oxon levels.
Since signiﬁcant inhibition is not predicted to occur until 5 mg/
kg, the model predicts adults will have slightly increased brain ace-
tylcholinesterase inhibition compared to children (Fig. 11C).
Simulations of time-course pharmacokinetics and biological
response also result in age-dependent patterns. Following a single
oral dose of 1 mg/kg chlorpyrifos, predicted time courses of
chlorpyrifos, chlorpyrifos-oxon, and inhibition of red blood cell
cholinesterase activity follow similar patterns as the respective
peak levels, where adults had the highest levels of chlorpyrifos
(as for all doses), and 6 months infants had the highest levels of
chlorpyrifos-oxon and red blood cell cholinesterase inhibition
(for doses >0.6 mg/kg) (Fig. 12). Adults had a higher AUC value of
chlorpyrifos concentration in blood and longer half-lives of chlor-
pyrifos in blood (Table 5). Infants of 6 months of age had a larger
AUC value of chlorpyrifos-oxon in blood. AUC values of TCPy in
blood and half-lives of chlorpyrifos-oxon and TCPy in blood were
very similar.
3.5. Sensitivity analysis
A sensitivity analysis was conducted on the life-stage PBPK/PD
model for peak inhibition of red blood cell and brain acetylcholin-
esterase activity. Of the selected parameters, red blood cell acetyl-
cholinesterase inhibition for both ages was most sensitive to blood
ﬂow to liver, fraction of chlorpyrifos-oxon bound in plasma, chlor-
pyrifos-oxon partition coefﬁcient in liver, acetylcholinesterase lev-
els in red blood cells, and chlorpyrifos metabolism in liver
(Table 6). Inhibition of acetylcholinesterase in brain for both ages
was most sensitive to brain chlorpyrifos desulfuration, hepatic
chlorpyrifos dearylation, hepatic chlorpyrifos-oxon hydrolysis,
brain volume, blood ﬂow to liver, acetylcholinesterase levels in
the brain, carboxylesterase levels in brain, carboxylesterase levels
in brain in liver, fractions of both chlorpyrifos and chlorpyrifos-
oxon bound in plasma, and chlorpyrifos partition coefﬁcients in
liver as well as brain (Table 6). Sensitive parameters were, for
the most part, consistent between both age groups. The only major
differences between age groups was for chlorpyrifos-oxon hydroly-
sis in blood and liver was sensitive in adults, where in 6 months
infants, other sequestrations of chlorpyrifos-oxon were more sen-
sitive (e.g. B-estereases). This could be due to higher capacities of
chlorpyrifos-oxon hydrolysis in adults.

D: Kisicki 2 mg/kg

C: Kisicki 1 mg/kg

B: Kisicki 0.5 mg/kg

A: Nolan
Plasma ChE
Fig. 8. Life-stage model predictions of cholinesterase (ChE) activities from human volunteer studies including plasma cholinesterase from a 0.5 mg/kg chlorpyrifos (CPF) (A)
(Nolan et al., 1984) and red blood cell cholinesterase activity (Kisicki et al., 1999; Timchalk et al., 2002), after being dosed with 0.5 (B), 1.0 (C), or 2 mg/kg (D) CPF.

4. Discussion
A life-stage PBPK/PD model for chlorpyrifos was developed to
predict chlorpyrifos disposition and biological response across
ages. Mathematical descriptions of age-dependent changes in body
weight, organ volumes, and metabolism from literature sources
and experimental studies were all incorporated into the model.
Finally, model simulations were compared to controlled adult
0.1

D
Plasma BuChE Activity
0.1

C
0.1

0.00001
0.1

B
CPF-oxon Conc. in Blood (µM)
0.1

0.1

A
Fig. 9. Life-stage model predictions of 6 months infants (dashed line), 3 yr old children (dotted line), and 30 yr old adults (solid line) exposed to a variety of chlorpyrifos (CPF)
doses. Predictions include peak chlorpyrifos concentration in blood (A), chlorpyrifos-oxon (CPF-oxon) concentrations in blood (B), minimal cholinesterase (ChE) activity in red
blood cells (C), and plasma (D). Note: y-axes in (A) and (B) are on a logarithmic scale, and x-axes are on a logarithmic scale.

0.0000
0.0005
0.0010
0.0015
0.0020
B
CPF-oxon Conc. in Blood (µM)

0.0
0.1
0.2
0.3
0.4
0.5
A

C
Fig. 10. Life-stage model predictions of humans dosed with 0.5 or 1 mg/kg chlorpyrifos (CPF) orally as a function of age. Predtictions include peak CPF concentration in blood
(A), chlorpyrifos-oxon (CPF-oxon) concentrations in blood (B), and minimum acetylcholinesterase (AChE) activity in red blood cells (RBC).

human exposure studies. Computational models provide a unique
framework to quantitatively incorporate various age-dependent
changes in physiology and mechanisms of chemical disposition
to predict net effects on target tissue dosimetry and biological
response.
Physiological values used in the PBPK/PD model were similar to
what others use in standard PBPK models. Compartment volumes
obtained from literature sources and reﬁt compartment volume
parameters were very consistent with standard adult PBPK volume
estimates (Fig. 3) (Brown et al., 1997) and other model estimates
from
our
group
including
adults
and
old
children
(Hinderliter et al., 2011). Overall, the sum of compartments within
the model (total volume of distribution) accounted for 75–95% of
body weight depending on age not including skeletal bone and
0.1

100 C
Brain AChE Activity
0.1

1.0 10-07
1.0 10-06
1.0 10-05
1.0 10-04
1.0 10-03
1.0 10-02
B
CPF-oxon Conc. in Brain (µM)
0.1

0.1

A
CPF Conc. in Brain (µM)
×
×
×
×
×
×
Fig. 11. Life-stage model predictions of 6 months infants (dashed line), 3 yr old children (dotted line), and 30 yr old adults (solid line) exposed to a variety of chlorpyrifos
(CPF) doses. Predictions include peak CPF concentration in brain (A), chlorpyrifos-oxon (CPF-oxon) concentrations in brain (B), and minimum acetylcholinesterase (AChE)
activity in brain. Note: y-axes in Fig. 10A and B are on a logarithmic scale, and x-axes are on a logarithmic scale.

100 B

---CHUNK_BREAK---

B are on a logarithmic scale, and x-axes are on a logarithmic scale. 100 B 0.1
1 A
Fig. 12. Time course life-stage model predictions of 6 months infants (dashed line), 3 yr old children (dotted line), and 30 yr old adults (solid line) exposed to 1 mg/kg
chlorpyrifos (CPF) dose. Predictions include CPF concentration in blood (A) and cholinesterase (ChE) activity in red blood cells (B). Note: y-axis in Fig. 11A is on a logarithmic
scale.
Table 5
Area under the curve (AUC) and half-lives (T1/2) of chlorpyrifos (CPF), chlorpyrifos-oxon (CPF-oxon), and 3,5,6-trichloro-2-pyridinol (TCPy) in blood as predicted for humans aged
0.5, 3, and 30 yr the life-stage model following an oral dose of 1 mg/kg chlorpyrifos.
CPF
0.5
3.4

3.9

3.76

0.008
3.9

5.31

0.007
3.6

non-adipose connective tissue (Supplemental Fig. 4). Blood ﬂows
were also consistent with standard adult values and previously
published values (Fig. 4) (Brown et al., 1997; Hinderliter et al.,
2011), and the overall cardiac output (summation of blood ﬂows)
was very similar to more commonly used allometric scaling meth-
ods (Brown et al., 1997) (Supplemental Fig. 8). Using the algorithm
approach to calculate the volume of distribution allowed for phys-
iological changes from birth to adulthood to be accounted for in
TCPy pharmacokinetics. Body weights are increasing with time
(Ogden et al., 2004), and thus the use of cross sectional physiolog-
ical data to simulate lifetime exposures may have some uncertain-
ties, especially for longer simulation times.
There have been some concerns raised that chlorpyrifos-oxon
hydrolysis previously measured in vitro (Smith et al., 2011) is not
relevant for PBPK modeling, because measurements were con-
ducted at non-physiological pH and salt concentration, and mea-
surements did not account for both A- and B-esterase hydrolysis
of chlorpyrifos-oxon (US EPA, 2011). Like many biological esti-
mates experimentally derived in vitro, measurements of oxon
hydrolysis have traditionally used experimental parameters (e.g.
pH and salt concentrations) optimized for the in vitro system,
which are not at standard physiological levels (Furlong et al.,
1989; Richter and Furlong, 1999). The signiﬁcance of using these
in vitro estimates measured at non-physiological conditions, how-
ever, is a bit unclear. Hydrolysis rates of diazoxon, a similar orga-
nophosphate pesticide, demonstrated no differences for QQ (the
most sensitive phenotype) and QR phenotypes incubated under
optimized
in
vitro
and
physiological
(Richter et al., 2009). Diazoxon hydrolysis rates of RR phenotypes
(least sensitive phenotype) were 16% slower in optimized in vitro
conditions compared to physiological conditions (Richter et al.,
2009). Additionally, chlorpyrifos-oxon hydrolysis in plasma was
measured under physiological conditions, and activities levels ran-
ged from 3 to 10 lmol/(min  mL) (Richter et al., 2009). Adult Vmax
values for chlorpyrifos-oxon hydrolysis in plasma used to parame-
terize the life-stage PBPK model were 4–9 lmol/(min  mL) (Smith
et al., 2011), which is very similar to those measured previously
under physiological conditions (Richter et al., 2009). Hepatic chlor-
pyrifos-oxon hydrolysis intrinsic clearance values used in the life-
stage PBPK model (Smith et al., 2011) are consistent with previ-
ously
reported
values
measured
at
physiological
(Sams et al., 2004). Using these metabolism estimates and opti-
mized transfer rates, the model accurately predicts available
human data (Figs. 5–8). Additional concerns have been raised
regarding not controlling for chlorpyrifos-oxon hydrolysis by B-
esterases while obtaining metabolism parameters for A-esterases
in vitro (US EPA, 2011). Here, we demonstrate that B-esterases
are completely inhibited by 500 nM of chlorpyrifos-oxon in human
plasma (Supplemental Fig. 7). This indicates that the relative
contribution of chlorpyrifos-oxon hydrolysis by B-esterases is
insigniﬁcant at experimental conditions used to measure Michaelis–
Menten
metabolism
kinetics
of
A-esterases
(72.3–2400 lM
chlorpyrifos-oxon in diluted [1/200] human plasma) (Smith et al.,
2011), as 1  104–3  103% of the chlorpyrifos-oxon would have
inhibited B-esterases in plasma. Similarly in rat liver homogenates,
it has been demonstrated that hepatic B-esterases are nearly
Table 6
Sensitivity analysis for selected parameters of the life-stage model following an oral dose of 3 lg/kg chlorpyrifos (CPF) for 6 months and 30 yr old humans. Endpoints included
acetylcholinesterase (AChE) inhibition in red blood cells and brain, and the sensitivity coefﬁcients were calculated at the time of maximal inhibition. Categories of sensitivity
include ‘‘Low’’ (absolute value of sensitivity coefﬁcient < 0.1), ‘‘Med’’ (absolute value of sensitivity coefﬁcient > 0. 1 and < 0.5), and ‘‘High’’ (absolute value of sensitivity
coefﬁcient > 0.5).
Sensitivity category
Red blood cell AChE Inhibition
Brain AChE Inhibition
6 months
6 months
Metabolism
Hepatic dearylation
Hepatic desulfuration
Med
Low
Hepatic CPF-oxon hydrolysis
Low
Blood CPF-oxon hydrolysis
Low
Low
Brain dearylation
Low
Low
Med
Med
Brain desulfuration
Low
Low
Compartment volume
Low
Low
Fat
Low
Low
Low
Low
Low
Low
Blood ﬂows
Low
Low
Low
Low
Med
Med
Enzyme levels
Red blood cell AChE
Low
Brain AChE
Low
Low
Liver carboxylesterase
Med
Brain carboxylesterase
Low
Fraction bound in plasma
CPF
Partition coeffcient
CPF
Low
Low
Low
Low
Fat
Low
Low
Low
Med
Low
Low
Low
Low
Low
Low
Fat
Low
Low
Low
Low

---CHUNK_BREAK---

Low Low Low Med Low Low Low Low Low Low Fat Low Low Low Low completely inhibited by 7.5 lM chlorpyrifos-oxon (Chanda et al.,
1997; Mortensen et al., 1998a). Thus, we feel that available
chlorpyrifos-oxon hydrolysis measurements are sufﬁcient for
parameterization of the life-stage model.
One difference between the previously published chlorpyrifos
model in preweanling rats and this model was the scaling of B-
esterase levels (acetyl-, butyryl-, and carboxyl-) (Timchalk et al.,
2007b). Experimental evidence suggests that overall levels of
acetyl- and butyryl-esterases increase with age in brain tissue of
rats (Liu et al., 1999; Mortensen et al., 1998b; Tang et al., 1999)
and were scaled allometically by body weight in the rat neonate
model (Timchalk et al., 2007b). However, these age-related differ-
ences were relatively insensitive when scaled by age-dependent
brain volume, as simulations of 1 and 5 mg/kg chlorpyrifos caused
an increase of brain cholinesterase inhibition by 1–3%, respec-
tively, when using the scaled parameters versus an overall mean
(data not shown). Due to the lack of sensitivity of these parameters
and the lack of available human data (speciﬁcally age-dependent
levels of B-esterases), these parameters were held constant and
scaled by brain volume in the life-stage PBPK/PD model. Likewise,
scaling cholinesterase activities by red blood cell and plasma vol-
umes resulted in adequate age-dependent scaling of experimental
values (Carr et al., 2001) and were handled as such in this life-stage
model. Carboxylesterase activity has also demonstrated increased
levels with age in the liver, plasma, and brain tissue of rats
(Atterberry et al., 1997; Chanda et al., 2002; Karanth and Pope,
2000; Lassiter et al., 1999). However, due to limited human data,
there is some uncertainty to whether this pattern persists across
species. Pope et al. (2005) measured carboxylesterase activity in
a limited number of human liver S9 fractions ages 2 months to
36 yr (n = 10) and found no statistical signiﬁcant relationship,
although samples from individuals 2 and 3 months old (the youn-
gest samples tested) had the lowest activities. Ontogeny of human
carboxylesterase expression has been measured in S9 liver frac-
tions, and it was found that expression of human carboxylester-
ase-1 was signiﬁcantly lower in children <1 yr of age, while
human carboxylesterase-2 demonstrated no signiﬁcant differences
across age (Zhu et al., 2009). Yang et al. (2009) reported expression
and activities for various drugs (e.g. aspirin, permethrin, etc.) for
both human carboxylesterase-1 and -2 demonstrated the following
pattern in pooled samples: fetuses < children < adults. The rela-
tionship between the relative expression of human carboxylester-
ase-1 and -2 with overall activity of carboxylesterase (measured
with p-nitrophenyl acetate hydrolysis) is unknown. In humans,
carboxylesterase is not found in plasma (Li et al., 2005), and no
studies have investigated the ontogeny of carboxylesterase activity
in brain tissue.
Other age-dependent factors were considered for incorporation
into the model but were instead held constant levels of microsomal
protein, overall levels of plasma proteins, and transfer rates. In rats,
it has been demonstrated that microsomal protein levels increase
from birth to postnatal day 7, where they approach adult levels
(Alcorn et al., 2007), and in humans, a meta-analysis suggests some
possibility of a similar trend existing in humans, although substan-
tial operator-speciﬁc error and inter-individual variability exists
(Barter et al., 2008). Because of that variability and small sample
size of pediatric samples compared to adults, hepatic microsome
levels are held constant in the life-stage PBPK/PD model. It was
previously reported that levels of plasma proteins increase with
age in humans (Alcorn and McNamara, 2003; Kanakoudi et al.,
1995; Smith et al., 2011). This could have implications on levels
of protein binding, especially at high exposures, as binding of
chlorpyrifos and chlorpyrifos-oxon in plasma were sensitive
parameters for both age groups in respect to brain acetylcholines-
terase inhibition at the reference dose (Table 6) and red blood cell
acetylcholinesterase inhibition at higher doses (data not shown).
However, since most risk-based model simulations focus on envi-
ronmental exposures, it was assumed that possible age-dependent
difference in plasma protein levels would have a negligible effect
on binding of low levels of chlorpyrifos and chlorpyrifos-oxon in
plasma, and fractional binding of chlorpyrifos and chlorpyrifos-
oxon was held constant in this model. Age-dependent transfer
rates with respect to chlorpyrifos pharmacokinetics have not been
investigated, and thus they were held constant in this model.
The life-stage PBPK/PD model predicts similar responses in
adults compared to previous PBPK/PD models for chlorpyrifos. Pre-
viously, a chlorpyrifos PBPK/PD model was published for adult rats
and humans (Timchalk et al., 2002). This life-stage model built
upon that model with several updates including partition coefﬁ-
cients, gut and brain metabolism, and age-dependent measures
such as metabolism and anatomy. In comparison to the previous
model, the life-stage model predicts very similar response in
plasma cholinesterase inhibition up to 6 lg/kg/d; afterwards, the
life-stage model predicts a more sensitive response (Fig. 13). Like-
wise, the life-stage model predicts more sensitive responses for
acetylcholinesterase inhibition in red blood cells once signiﬁcant
inhibition occurs and a very similar response in brain acetylcholin-
esterase inhibition (Fig. 13). Parameter updates to the original
model all contribute, to some degree, to these differences.
The life-stage model predicts age-dependent differences in
and
biological
response.
After
equivalent oral doses of chlorpyrifos, the life-stage model predicts
marginally lower systemic levels of chlorpyrifos and, at doses
P0.6 mg/kg chlorpyrifos, higher levels of chlorpyrifos-oxon in chil-
dren compared to adults. These age-dependent discrepancies
resulted from differences in overall chlorpyrifos and chlorpyrifos-
oxon metabolism and, to a lesser extent, chlorpyrifos distribution.
Higher chlorpyrifos levels in adults resulted from lower levels of
chlorpyrifos metabolism compared to children on a body weight
basis as evidenced by a larger AUC of chlorpyrifos in blood and
longer chlorpyrifos blood half-life (Table 5). Since levels of hepatic
chlorpyrifos and chlorpyrifos-oxon metabolism on a microsomal
basis and the level of hepatic microsomal protein are constant as
a function of age in the model, increased hepatic chlorpyrifos and
chlorpyrifos-oxon metabolism in children is driven by a larger liver
fraction per body weight compared to adults. At doses P0.6 mg/kg
(100- to 1000-fold higher than environmental exposure levels),
predicted increases in chlorpyrifos-oxon in children are a result
of
levels
overwhelming
metabolism capacity in plasma, which is lower in children than
in adults (Smith et al., 2011). At doses <0.6 mg/kg, increased chlor-
pyrifos-oxon metabolism in children is enough to cause marginally
lower chlorpyrifos-oxon levels compared to adults. The model pre-
dicts that plasma cholinesterase inhibition is slightly higher in
0.1

10000

CPF Dose (µg/kg/day)
Percent Activity
Fig. 13. Comparison of cholinesterase inhibition in plasma and acetylcholinesterase
inhibition in red blood cells and brain between the life-stage physiologically based
pharmacokinetic and pharmacodynamic (PBPK/PD) model (solid lines) and a
previously published PBPK/PD model (dashed lines) for chlorpyrifos (CPF) in adults.
Single doses were administered as zero order constant rates of uptake for both
simulations.

---CHUNK_BREAK---

adults. Single doses were administered as zero order constant rates of uptake for both simulations. adults than in children, because the dynamic range for cholinester-
ase inhibition in plasma occurs at doses lower than 0.6 mg/kg
chlorpyrifos, and thus, chlorpyrifos-oxon levels are slightly higher
in adults. These simulations (<0.6 mg/kg chlorpyrifos) are compa-
rable to predictions made previously, suggesting that 19-year old
humans are more sensitive to plasma and red blood cell cholines-
terase inhibition than 1-year olds from equivalent oral doses of
chlorpyrifos (Foxenberg et al., 2011). Besides metabolism, distribution also plays a role in age-depen-
dent differences in chlorpyrifos pharmacokinetics. Adults have
more fat content than children, and since chlorpyrifos is lipophilic
(logKow 4.82; McCall et al., 1980), fat can act as a chlorpyrifos
depot. Following an oral dose of chlorpyrifos, adults have a larger
fraction of the dose in fat depots compared to 6 months infants
(2-fold), which alters the distribution of chlorpyrifos. Lower over-
all chlorpyrifos metabolism and, at a lesser extent, altered distribu-
tion increases the half-life of chlorpyrifos in blood to nearly double
in adults compared to 6 months old neonates (Table 5). Dietary exposure is considered to be the primary route of non-
occupational chlorpyrifos exposure (Lu et al., 2010). CARES and
LifeLine are two dietary exposure models that have predicted CPF
exposure levels (Price et al., 2011). CARES predicted 11 (2.7–47)
and 3.4 (0.8–15) ng/kg/d median (95% conﬁdence intervals) CPF
exposure for children and adults, respectively; while LifeLine pre-
dicted 20 (4.7–67) and 5.7 (1.2–24) ng/kg/d for children and adults
(Price et al., 2011). These levels are well below the threshold
(0.6 mg/kg) where the life-stage model predicts children to be more
sensitive than adults to chlorpyrifos from equivalent oral doses. There is uncertainty regarding model simulations of the brain
compartment. Recently, the potential importance of low-level
brain metabolism has been suggested especially for exposure
routes that lead to higher levels of chlorpyrifos in blood by circum-
venting ﬁrst pass metabolism in oral exposures (Ellison et al.,
2011; Smith et al., 2009). Here, high sensitivity coefﬁcients for
parameters describing chlorpyrifos desulfuration in brain calcu-
lated at a reference dose for all ages further highlight this issue. In the life-stage model, estimates of brain metabolism are derived
from
preliminary
metabolism
studies
with
rat
brain
tissue
(Timchalk et al., 2012). Experimentally derived measures of carb-
oxylesterase and PON1 activities in brain tissue are rare in adult
humans and do not exist for infants or children. Thus with the lack
of experimental data, there remains a high degree of uncertainty
surrounding quantitative predictions of the brain compartment,
and additional experimental focus on this area may be warranted. A life-stage PBPK/PD model for chlorpyrifos in humans has been
developed. The model was calibrated and validated against con-
trolled adult human exposure studies. Simulations suggest age-
dependent pharmacokinetics and response exist, where at doses
P0.6 mg/kg, children have higher levels of chlorpyrifos-oxon in
blood and higher levels of red blood cell cholinesterase inhibition
from equivalent oral doses of chlorpyrifos. At doses <0.6, the model
predicts that adults will have slightly higher levels of chlorpyrifos-
oxon in blood, and thus inhibition of cholinesterase as well. It is
important to note that these simulations are made at ages that
the model has not been validated in vivo, as data from children
exposed to pesticides are very rare and difﬁcult to obtain. Until
such data exists, authors feel that this model provides a strategy
to make reasonable predictions regarding life-stage pharmacoki-
netics and response. In the future, this model will have variability
of sensitive parameters incorporated into the model structure and
linked to exposure models to predict a life-stage based population
response to environmental levels of chlorpyrifos. Conﬂict of interest
None. Acknowledgments
Funding for this project was provided by the Dow AgroSciences,
LLC. Appendix A. Supplementary data
Supplementary data associated with this article can be found,
in the online version, at http://dx.doi.org/10.1016/j.yrtph.2013. 10.005. References
ICRP Publication 89, 2002. Basic anatomical and physiological data for use in
radiological protection: reference values. A report of age- and gender-related
differences in the anatomical and physiological characteristics of reference
individuals. Ann. ICRP 32, 5–265. Albers, J., Garabrant, D., Berent, S., Richardson, R., 2010. Paraoxonase status and
plasma butyrylcholinesterase activity in chlorpyrifos manufacturing workers. J. Expo. Sci. Environ. Epidemiol. 20, 79–89. Alcorn, J., Elbarbry, F.A., Allouh, M.Z., McNamara, P.J., 2007. Evaluation of the
assumptions of an ontogeny model of rat hepatic cytochrome P450 activity. Drug Metab. Dispos. 35, 2225–2231. Alcorn, J., McNamara, P.J., 2003. Pharmacokinetics in the newborn. Adv. Drug Deliv. Rev. 55, 667–686. Atterberry, T.T., Burnett, W.T., Chambers, J.E., 1997. Age-related differences in
parathion and chlorpyrifos toxicity in male rats: target and nontarget esterase
sensitivity
and
cytochrome
P450-mediated
metabolism. Toxicol. Appl. Pharmacol. 147, 411–418. Bakke, J.E., Feil, V.J., Price, C.E., 1976. Rat urinary metabolites from O, O-diethyl-O-
(3,5,6-trichloro-2-pyridyl) phosphorothioate. J. Environ. Sci. Health B 11, 225–
230. Barter, Z.E., Chowdry, J.E., Harlow, J.R., Snawder, J.E., Lipscomb, J.C., Rostami-
Hodjegan, A., 2008. Covariation of human microsomal protein per gram of liver
with age: absence of inﬂuence of operator and sample storage may justify
interlaboratory data pooling. Drug Metab. Dispos. 36, 2405–2409. Brown, R.P., Delp, M.D., Lindstedt, S.L., Rhomberg, L.R., Beliles, R.P., 1997. Physiological parameter values for physiologically based pharmacokinetic
models. Toxicol. Ind. Health 13, 407–484. Bruckner, J.V., 2000. Differences in sensitivity of children and adults to chemical
toxicity: the NAS panel report. Regul. Toxicol. Pharmcol. 31, 280–285. Busby-Hjerpe, A.L., Campbell, J.A., Smith, J.N., Lee, S., Poet, T.S., Barr, D., Timchalk, C.,
2010. Comparative
of
versus
its
major
metabolites following oral administration in the rat. Toxicology 268, 55–63. Carr, R.L., Chambers, H.W., Guarisco, J.A., Richardson, J.R., Tang, J., Chambers, J.E.,
2001. Effects of repeated oral postnatal exposure to chlorpyrifos on open-ﬁeld
behavior in juvenile rats. Toxicol. Sci. 59, 260–267. Chanda, S.M., Lassiter, T.L., Moser, V.C., Barone, S., Padilla, S., 2002. Tissue
carboxylesterases and chlorpyrifos toxicity in the developing rat. Hum. Ecol. Risk Assess. 8, 75–90. Chanda, S.M., Mortensen, S.R., Moser, V.C., Padilla, S., 1997. Tissue-speciﬁc effects of
chlorpyrifos on carboxylesterase and cholinesterase activity in adult rats: an
in vitro and in vivo comparison. Fundam. Appl. Toxicol. 38, 148–157. Clewell, R.A., Merrill, E.A., Gearhart, J.M., Robinson, P.J., Sterner, T.R., Mattie, D.R.,
Clewell 3rd, H.J., 2007. Perchlorate and radioiodide kinetics across life stages in
the human: using PBPK models to predict dosimetry and thyroid inhibition and
sensitive subpopulations based on developmental stage. J. Toxicol. Environ. Health A 70, 408–428. Ellison, C.A., Smith, J.N., Lein, P.J., Olson, J.R., 2011. Pharmacokinetics and
pharmacodynamics of chlorpyrifos in adult male Long-Evans rats following
repeated subcutaneous exposure to chlorpyrifos. Toxicology 287, 137–144. Ellman, G.L., Courtney, K.D., Andres Jr., V., Feather-Stone, R.M., 1961. A new and
rapid colorimetric determination of acetylcholinesterase activity. Biochem. Pharmacol. 7, 88–95. Foxenberg, R.J., Ellison, C.A., Knaak, J.B., Ma, C., Olson, J.R., 2011. Cytochrome P450-
speciﬁc
human
PBPK/PD
models
for
the
organophosphorus
pesticides:
chlorpyrifos and parathion. Toxicology 285, 57–66. Furlong,
C.E.,
Richter,
R.J.,
Seidel,
S.L.,
Costa,
L.G.,
Motulsky,
A.G.,
1989.

---CHUNK_BREAK---

parathion. Toxicology 285, 57–66. Furlong, C.E., Richter, R.J., Seidel, S.L., Costa, L.G., Motulsky, A.G., 1989. Spectrophotometric
assays
for
the
enzymatic
hydrolysis
of
the
active
metabolites
of
and
parathion
by
plasma
paraoxonase/
arylesterase.

Anal.

Biochem.

180, 242–247.

Gearhart, J.M., Jepson, G.W., Clewell 3rd, H.J., Andersen, M.E., Conolly, R.B., 1990.

Physiologically based pharmacokinetic and pharmacodynamic model for the
inhibition of acetylcholinesterase by diisopropylﬂuorophosphate.

Toxicol.

Appl.

Pharmacol.

106, 295–310.

Ginsberg, G., Hattis, D., Russ, A., Sonawane, B., 2004.

Physiologically based
pharmacokinetic (PBPK) modeling of caffeine and theophylline in neonates
and adults: implications for assessing children’s risks from environmental
agents.

J.

Toxicol.

Environ.

Health A 67, 297–329.

Hinderliter, P.M., Price, P.S., Bartels, M.J., Timchalk, C., Poet, T.S., 2011.

Development
of a source-to-outcome model for dietary exposures to insecticide residues: an
example using chlorpyrifos.

Regul.

Toxicol.

Pharmcol.

61, 82–92.

---CHUNK_BREAK---

for dietary exposures to insecticide residues: an example using chlorpyrifos. Regul. Toxicol. Pharmcol. 61, 82–92. Hojring, N., Svensmark, O., 1976. Carboxylesterases with defferent substrate
speciﬁcity in human brain extracts. J. Neurochem. 27, 525–528. Janssen, I., Heymsﬁeld, S.B., Wang, Z.M., Ross, R., 2000. Skeletal muscle mass
and distribution in 468 men and women aged 18–88 yr. J. Appl. Physiol. 89,
81–88. Kamataki, T., Lee Lin, M.C., Belcher, D.H., Neal, R.A., 1976. Studies of the metabolism
of parathion with an apparently homogeneous preparation of rabbit liver
cytochrome P-450. Drug. Metab. Dispos. 4, 180–189. Kanakoudi, F., Drossou, V., Tzimouli, V., Diamanti, E., Konstantinidis, T., Germenis,
A., Kremenopoulos, G., 1995. Serum concentrations of 10 acute-phase proteins
in healthy term and preterm infants from birth to age 6 months. Clin. Chem. 41,
605–608. Karanth, S., Pope, C., 2000. Carboxylesterase and A-esterase activities during
maturation and aging: relationship to the toxicity of chlorpyrifos and parathion
in rats. Toxicol. Sci. 58, 282–289. Kisicki, J.C., Seip, C.W., Combs, M.L., 1999. A rising dose toxicology study to
determine
the
no-observable-effect-levels
(NOEL)
for
erythrocyte
acetylcholinesterase (AChE) inhibition and cholinergic signs and symptoms of
chlorpyrifos at three dose levels. The Toxicology Research Laboratory: Health
and Environmental Research Laboratories, The DOW Chemical Company
(Results published in Timchalk et al. 2002), Midland, MI, USA. Kousba, A.A., Poet, T.S., Timchalk, C., 2007. Age-related brain cholinesterase
inhibition kinetics following in vitro incubation with chlorpyrifos-oxon and
diazinon-oxon. Toxicol. Sci. 95, 147–155. Kousba,
A.A.,
Sultatos,
L.G.,
Poet,
T.S.,
Timchalk,
C.,
2004. Comparison
of
chlorpyrifos-oxon and paraoxon acetylcholinesterase inhibition dynamics:
potential role of a peripheral binding site. Toxicol. Sci. 80, 239–248. Lafortuna, C.L., Mafﬁuletti, N.A., Agosti, F., Sartorio, A., 2005. Gender variations of
body composition, muscle strength and power output in morbid obesity. Int. J. Obes. 29, 833–841. Lassiter, T.L., Barone Jr., S., Moser, V.C., Padilla, S., 1999. Gestational exposure to
chlorpyrifos: dose response proﬁles for cholinesterase and carboxylesterase
activity. Toxicol. Sci. 52, 92–100. Li, B., Sedlacek, M., Manoharan, I., Boopathy, R., Duysen, E.G., Masson, P., Lockridge,
O., 2005. Butyrylcholinesterase, paraoxonase, and albumin esterase, but not
carboxylesterase, are present in human plasma. Biochem. Pharmacol. 70, 1673–
1684. Liao, K.H., Tan, Y.M., Conolly, R.B., Borghoff, S.J., Gargas, M.L., Andersen, M.E., Clewell
3rd, H.J., 2007. Bayesian estimation of pharmacokinetic and pharmacodynamic
parameters in a mode-of-action-based cancer risk assessment for chloroform. Risk Anal. 27, 1535–1551. Lipscomb, J.C., Poet, T.S., 2008. In vitro measurements of metabolism for application
in pharmacokinetic modeling. Pharmacol. Ther. 118, 82–103. Liu, J., Olivier, K., Pope, C.N., 1999. Comparative neurochemical effects of repeated
methyl parathion or chlorpyrifos exposures in neonatal and adult rats. Toxicol. Appl. Pharmacol. 158, 186–196. Lowe, E.R., Poet, T.S., Rick, D.L., Marty, M.S., Mattson, J.L., Timchalk, C., Bartels, M.J.,
2009. The effect of plasma lipids on the pharmacokinetics of chlorpyrifos and
the impact on interpretation of blood biomonitoring data. Toxicol. Sci. 108,
258–272. Lu, C., Holbrook, C.M., Andres, L.M., 2010. The implications of using a physiologically
based pharmacokinetic (PBPK) model for pesticide risk assessment. Environ. Health Perspect. 118, 125–130. Luecke, R.H., Pearce, B.A., Wosilait, W.D., Slikker Jr., W., Young, J.F., 2007. Postnatal
growth considerations for PBPK modeling. J. Toxicol. Environ. Health A 70,
1027–1037. Marty, M.S., Andrus, A.K., Bell, M.P., Passage, J.K., Perala, A.W., Brzak, K.A., Bartels,
M.J., Beck, M., Juberg, D.R., 2012. Cholinesterase inhibition and toxicokinetics in
immature and adult rats after acute or repeated exposures to chlorpyrifos or
chlorpyrifos-oxon. Regul. Toxicol. Pharmacol. 63, 209–224. Maxwell, D.M., Lenz, D.E., Groff, W.A., Kaminskis, A., Froehlich, H.L., 1987. The
effects of blood ﬂow and detoxiﬁcation on in vivo cholinesterase inhibition by
soman in rats. Toxicol. Appl. Pharmacol. 88, 66–76. McCall, P.J., Swann, R.L., Laskowski, D.A., Unger, S.M., Vrona, S.A., Dishburger, H.J.,
1980. Estimation of chemical mobility in soil from liquid chromatographic
retention times. Bull. Environ. Contam. Toxicol. 24, 190–195. Mortensen, S.R., Brimijoin, S., Hooper, M.J., Padilla, S., 1998a. Comparison of the
in vitro sensitivity of rat acetylcholinesterase to chlorpyrifos-oxon: what do
tissue IC50 values represent? Toxicol. Appl. Pharmacol. 148, 46–49. Mortensen, S.R., Hooper, M.J., Padilla, S., 1998b. Rat brain acetylcholinesterase
activity: developmental proﬁle and maturational sensitivity to carbamate and
organophosphorus inhibitors. Toxicology 125, 13–19. Nolan,
R.J.,
Rick,
D.L.,
Freshour,
N.L.,
Saunders,
J.H.,
1984. Chlorpyrifos:
pharmacokinetics in human volunteers. Toxicol. Appl. Pharmacol. 73, 8–15. Ogden, C.L., Fryar, C.D., Carroll, M.D., Flegal, K.M., 2004. Mean body weight, height,
and body mass index, United States 1960–2002. Adv. Data., 1–17. Poet, T.S., Hinderliter, P.M., Timchalk, C., Smith, J.N., Bartels, M.J., McDougal, R.,
Price, P., in preparation. Application of a human life-stage physiologically based
pharmacokinetic and pharmacodynamic model for chlorpyrifos: uncertainty
and inter-individual variation in risk assessment. Poet, T.S., Wu, H., Kousba, A.A., Timchalk, C., 2003. In vitro rat hepatic and intestinal
metabolism of the organophosphate pesticides chlorpyrifos and diazinon. Toxicol. Sci. 72, 193–200. Pond, A.L., Chambers, H.W., Coyne, C.P., Chambers, J.E., 1998. Puriﬁcation of two rat
hepatic
proteins
with
A-esterase
activity
toward
and
paraoxon. J. Pharmacol. Exp. Ther. 286, 1404–1411. Pope, C.N., Chakraborti, T.K., Chapman, M.L., Farrar, J.D., Arthun, D., 1991. Comparison of in vivo cholinesterase inhibition in neonatal and adult rats by
three organophosphorothioate insecticides. Toxicology 68, 51–61. Pope, C.N., Karanth, S., Liu, J., Yan, B., 2005. Comparative carboxylesterase activities
in infant and adult liver and their in vitro sensitivity to chlorpyrifos oxon. Regul. Toxicol. Pharmacol. 42, 64–69. Poulin, P., Haddad, S., 2011. Microsome composition-based model as a mechanistic
tool to predict nonspeciﬁc binding of drugs in liver microsomes. J. Pharm. Sci. 100, 4501–4517. Poulin, P., Kenny, J.R., Hop, C.E., Haddad, S., 2011. In vitro-in vivo extrapolation of
clearance: modeling hepatic metabolic clearance of highly bound drugs and
comparative assessment with existing calculation methods. J. Pharm. Sci. 101,
838–851. Poulin, P., Krishnan, K., 1995. An algorithm for predicting tissue: blood partition
coefﬁcients of organic chemicals from n-octanol: water partition coefﬁcient
data. J. Toxicol. Environ. Health 46, 117–129. Price, P.S., Schnelle, K.D., Cleveland, C.B., Bartels, M.J., Hinderliter, P.M., Timchalk, C.,
Poet, T.S., 2011. Application of a source-to-outcome model for the assessment of
health impacts from dietary exposures to insecticide residues. Regul. Toxicol. Pharmcol. 61, 23–31. Reiss, R., Neal, B., Lamb, J.C.t., Juberg, D.R., 2012. Acetylcholinesterase inhibition
dose-response modeling for chlorpyrifos and chlorpyrifos-oxon. Regul. Toxicol. Pharmacol. 63, 124–131. Richter, R.J., Furlong, C.E., 1999. Determination of paraoxonase (PON1) status
requires more than genotyping. Pharmacogenetics 9, 745–753. Richter, R.J., Jarvik, G.P., Furlong, C.E., 2009. Paraoxonase 1 (PON1) status and
substrate hydrolysis. Toxicol. Appl. Pharmacol. 235, 1–9. Sams, C., Cocker, J., Lennard, M.S., 2004. Biotransformation of chlorpyrifos and
diazinon by human liver microsomes and recombinant human cytochrome
P450s (CYP). Xenobiotica 34, 861–873. Schmitt, W., 2008. General approach for the calculation of tissue to plasma partition
coefﬁcients. Toxicol. In Vitro 22, 457–467. Sidell, F.R., Kaminskis, A., 1975. Inﬂuence of age, sex, and oral contraceptives on
human blood cholinesterase activity. Clin. Chem. 21, 1393–1395.

---CHUNK_BREAK---

of age, sex, and oral contraceptives on human blood cholinesterase activity. Clin. Chem. 21, 1393–1395. Smith, J.N., Campbell, J.A., Busby-Hjerpe, A.L., Lee, S., Poet, T.S., Barr, D.B., Timchalk,
C., 2009.

Comparative chlorpyrifos pharmacokinetics via multiple routes
of exposure and vehicles of administration in the adult rat.

Toxicology 261,
47–58.

Smith, J.N., Timchalk, C., Bartels, M.J., Poet, T.S., 2011.

In vitro age-dependent
enzymatic metabolism of chlorpyrifos and chlorpyrifos-oxon in human hepatic
microsomes and chlorpyrifos-oxon in plasma.

Drug Metab.

Dispos.

39, 1353–
1362.

Smith, J.N., Wang, J., Lin, Y., Timchalk, C., 2010.

Pharmacokinetics of the chlorpyrifos
metabolite 3,5,6-trichloro-2-pyridinol (TCPy) in rat saliva.

Toxicol.

Sci.

113,
315–325.

Sultatos, L.G., 1994.

Mammalian toxicology of organophosphorus pesticides.

J.

Toxicol.

Environ.

Health 43, 271–289.

Tang, J., Carr, R.L., Chambers, J.E., 1999.

Changes in rat brain cholinesterase activity
and muscarinic receptor density during and after repeated oral exposure to
chlorpyrifos in early postnatal development.

Toxicol.

Sci.

51, 265–272.

Timchalk, C., Busby, A., Campbell, J.A., Needham, L.L., Barr, D.B., 2007a.

Comparative
pharmacokinetics of the organophosphorus insecticide chlorpyrifos and its
major metabolites diethylphosphate, diethylthiophosphate and 3,5,6-trichloro-
2-pyridinol in the rat.

Toxicology 237, 145–157.

Timchalk, C., Kousba, A.A., Poet, T.S., 2007b.

An age-dependent physiologically
based pharmacokinetic/pharmacodynamic model for the organophosphorus
insecticide chlorpyrifos in the preweanling rat.

Toxicol.

Sci.

98, 348–365.

Timchalk, C., Nolan, R.J., Mendrala, A.L., Dittenber, D.A., Brzak, K.A., Mattsson, J.L.,
2002.

A Physiologically based pharmacokinetic and pharmacodynamic (PBPK/
PD) model for the organophosphate insecticide chlorpyrifos in rats and humans.

Toxicol.

Sci.

66, 34–53.

Timchalk,
C.,
Poet,
T.S.,
2008.

Development
of
a
physiologically
based
pharmacokinetic and pharmacodynamic model to determine dosimetry and
cholinesterase inhibition for a binary mixture of chlorpyrifos and diazinon in
the rat.

Neurotoxicology 29, 428–443.

Timchalk, C., Poet, T.S., Kousba, A.A., 2006.

Age-dependent pharmacokinetic and
pharmacodynamic response in preweanling rats following oral exposure to the
organophosphorus insecticide chlorpyrifos.

Toxicology 220, 13–25.

Timchalk, C., Smith, J., Hjerpe, A., Poet, T., Lee, S., 2012.

Regional brain dosimetry for
the organophosphorus insecticide chlorpyrifos in the preweanling rat.

In:
Knaak, J.B., Timchalk, C., Tornero-Velez, R.

(eds.), Parameters for Pesticide QSAR
and PBPK/PD Models for Human Risk Assessment.

ACS Symposium Series.

American Chemical Society, Washington, DC, USA.

US EPA, 2006.

A Framework for Assessing Health Risks of Environmental Exposures
to Children.

National Center for Environmental Assessment, Washington, DC;
EPA/600/R-05/093F.

US EPA, 2011.

Fungicide, and Rodenticide Act (FIFRA), Scientiﬁc Advisory Panel
(SAP)
Meeting
(2011-03)
Minutes:
Chlorpyrifos
Physiologically
Based
Pharmacokinetic
and
Pharmacodynamic
(PBPK/PD)
Modeling
Linked
to
Cumulative and Aggregate Risk Evaluation System (CARES), Washington, DC.

US NRC, 1993.

Pesticides in the Diets of Infants and Children.

Council Committee on
Pesticides in the Diets of Infants and Children.

National Academy Press,
Washington, DC, USA.

Vidair,
C.A.,
2004.

Age
dependence
of
organophosphate
and
carbamate
neurotoxicity in the postnatal rat: extrapolation to the human.

Toxicol.

Appl.

Pharmacol.

196, 287–302.

Whitney, K.D., Seidler, F.J., Slotkin, T.A., 1995. Developmental neurotoxicity of
chlorpyrifos: cellular mechanisms. Toxicol. Appl. Pharmacol. 134, 53–62.
Willhite, C.C., Ball, G.L., McLellan, C.J., 2008. Derivation of a bisphenol A oral
reference dose (RfD) and drinking-water equivalent concentration. J. Toxicol.
Environ. Health B Crit. Rev. 11, 69–146.
Wilson, Z.E., Rostami-Hodjegan, A., Burn, J.L., Tooley, A., Boyle, J., Ellis, S.W., Tucker,
G.T., 2003. Inter-individual variability in levels of human microsomal protein
and hepatocellularity per gram of liver. Br. J. Clin. Pharmacol. 56, 433–440.
Yang, D., Pearce, R.E., Wang, X., Gaedigk, R., Wan, Y.J., Yan, B., 2009. Human
carboxylesterases HCE1 and HCE2: ontogenic expression, inter-individual
variability and differential hydrolysis of oseltamivir, aspirin, deltamethrin and
permethrin. Biochem. Pharmacol. 77, 238–247.
Young, J.F., Luecke, R.H., Pearce, B.A., Lee, T., Ahn, H., Baek, S., Moon, H., Dye, D.W.,
Davis, T.M., Taylor, S.J., 2009. Human organ/tissue growth algorithms that
include obese individuals and black/white population organ weight similarities
from autopsy data. J. Toxicol. Environ. Health A 72, 527–540.
Zheng, Q., Olivier, K., Won, Y.K., Pope, C.N., 2000. Comparative cholinergic
neurotoxicity of oral chlorpyrifos exposures in preweanling and adult rats.
Toxicol. Sci. 55, 124–132.
Zhu, H.J., Appel, D.I., Jiang, Y., Markowitz, J.S., 2009. Age- and sex-related expression
and activity of carboxylesterase 1 and 2 in mouse and human liver. Drug Metab.
Dispos. 37, 1819–1825.