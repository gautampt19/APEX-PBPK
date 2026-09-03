TUTORIAL
Applied Concepts in PBPK Modeling: How to Build a
PBPK/PD Model
L Kuepfer1, C Niederalt1, T Wendl1, J-F Schlender1, S Willmann2, J Lippert2, M Block1, T Eissing1 and D Teutonico1,3*
The aim of this tutorial is to introduce the fundamental concepts of physiologically based pharmacokinetic/pharmacodynamic
(PBPK/PD) modeling with a special focus on their practical implementation in a typical PBPK model building workflow. To
illustrate basic steps in PBPK model building, a PBPK model for ciprofloxacin will be constructed and coupled to a
pharmacodynamic model to simulate the antibacterial activity of ciprofloxacin treatment.
CPT Pharmacometrics Syst. Pharmacol. (2016) 5, 516–531; doi:10.1002/psp4.12134; published online 21 September 2016.
GENERAL INTRODUCTION TO PBPK MODELING
Overview of PBPK
In recent decades, different types of computational models
have been applied in drug development programs. PBPK
models combine information on the drug with independent
prior knowledge on the physiology and biology at the organ-
ism level to achieve a mechanistic representation of the
drug in biological systems, allowing the a priori simulation
of drug concentration–time profiles. Since PBPK models
explicitly consider different organs and tissues, it is possible
to obtain the quantitative characterization of concentration–
time profiles in the respective compartments. Such predic-
tion is of high pharmacological relevance since it enables
the estimation of drug exposure not only in plasma but also
at the site of action, which may be difficult or impossible to
measure experimentally.
A whole-body PBPK model (Figure 1a) contains an
explicit representation of the organs that are most relevant
to the absorption, distribution, excretion, and metabolization
of the drug due to their physiological/pharmacological func-
tion or their volume.1 These are typically heart, lung, brain,
stomach, spleen, pancreas, gut, liver, kidney, gonads, thy-
mus, adipose tissue, muscle, bone, and skin. The tissues
are linked by the arterial and venous blood compartments,
and each one of them is characterized by an associated
blood-flow rate, volume, tissue-partition coefficient, and per-
meability. A major advantage of PBPK modeling is the
availability of a comprehensive structural representation of
the physiology of an organism. The various parameters in
the model are either obtained from compilations of prior
knowledge or may be calculated from specific and carefully
validated formulas. From a general point of view, it is possi-
ble to distinguish between organism parameters on the one
hand and drug parameters on the other.
Figure 1b represents the hierarchical relationship of the
most important parameters in a PBPK model. The organ-
ism parameters are usually used as direct input in the mod-
el, representing the knowledge available a priori on the
anatomy and physiology. When dedicated software pack-
ages are used, such information is usually contained in the
database of the PBPK software available. By contrast, the
drug parameters in the model are related to the compound
partition coefficient and permeability across biological mem-
branes. In some cases such parameters can be measured
in vivo or in vitro, but most often they are estimated from
the physicochemical properties of the drug. In this context,
physicochemical parameters act as surrogate parameters
for the calculation of the compound distribution. For this
reason they can, in some cases, differ from the correspond-
ing measured value. This is particularly evident in the case
of lipophilicity, since this parameter is usually measured
under experimental in vitro conditions (e.g., octanol-water
partitioning) which do not match in vivo conditions in the
biological environment. Usually the calculation of membrane
permeabilities or partition coefficients is automatically per-
formed by the PBPK software. The latter parameters are
estimated
from so-called
distribution models quantifying
equilibrium between plasma and the surrounding tissue. As
an example, in Figure 1c the tissue and plasma concentra-
tions of theophylline estimated from its physicochemical
properties using different distribution models are illustrated.
As can be seen, the different models simulate different con-
centrations in the different organs; this point will be dis-
cussed in more detail in the section “Distribution models”
(below).
While passive processes can be calculated from such
model-based relationships, there is currently no similar meth-
od for a priori prediction of the kinetics of active processes
(e.g., metabolism, target binding, or active transport of the
drug). One way to quantify the contribution of different organs
to total clearance at the whole-body level is use of in vitro–in
vivo extrapolation.2 Furthermore, the relative tissue-specific
expression of genes or proteins might be considered.3 An
example of gene expression data is shown in Figure 1d,
where the relative expression normalized to the tissue with
the highest expression is represented for a group of enzymes,
in healthy individuals and cancer patients, respectively, as
well as for receptors and transporters in healthy individuals.
The PBPK models are composed of different types of
information that are combined during model building and
1Bayer Technology Services, Leverkusen, Germany; 2Bayer HealthCare, Wuppertal, Germany; 3Corresponding author current address: Clinical PK & Pharmacometrics,
Institut de Recherches Internationales Servier, 50, rue Carnot, 92284 Suresnes cedex, France. *Correspondence: D Teutonico (donato.teutonico@servier.com)
Received 13 April 2016; accepted 9 September 2016; published online on 21 September 2016. doi:10.1002/psp4.12134
Citation: CPT Pharmacometrics Syst. Pharmacol. (2016) 5, 516–531;
doi:10.1002/psp4.12134
V
C 2016 ASCPT
All rights reserved

---CHUNK_BREAK---

CPT Pharmacometrics Syst. Pharmacol. (2016) 5, 516–531; doi:10.1002/psp4.12134 V C 2016 ASCPT All rights reserved that can be used to generate simulations of different treat-
ment scenarios. Such building blocks of information includ-
ed in the model can be divided into organism properties,
drug properties, and administration protocol and formulation
properties, respectively (Figure 2).
Organism properties are, for instance, organ volumes,
organ composition, blood flows, surface areas, and expres-
sion levels. Such properties are dependent on the species
or population considered. For example, in the case of spe-
cial populations (e.g., diseased or pediatric populations)
these organism properties take into account physiological
differences between the special populations and the healthy
adult reference population. By combining the drug proper-
ties with the anatomical and physiological features of the
organism, it is possible to estimate the parameters for pas-
sive processes involved in distributing the drug in the body,
such as, for example, permeation across membranes.
Drug properties include all parameters specific for the
compounds under study. Notably, physicochemical proper-
ties such as compound lipophilicity, solubility, molecular
weight
(MW),
and
pKa
values
of
a
are
fully
independent of organism physiology. Drug-biological proper-
ties (such as fraction of drug unbound, or tissue-plasma
partition coefficient), on the other hand, are drug-specific
but also defined by the interaction between the drug and
the biological system itself, so they are dependent on both
the drug and the organism properties.
Finally, information on the administration protocol and for-
mulation properties is needed to define a PBPK simulation.
Time-related special events such as gallbladder emptying
time or meal intake can also be included in the model and
their impact on drug PK can be evaluated with the model.
The use of complex full-blown PBPK models was recently
facilitated by the development of several commercial plat-
forms that integrate physiological databases and implement
PBPK modeling approaches, such as GastroPlus (Simula-
tions Plus, Lancaster, PA), SimCyp (SimCyp, Sheffield,
UK), and PK-Sim and MoBi (Bayer Technology Services,
Leverkusen, Germany). These commercial PBPK modeling
platforms provide a generic model structure for the physiol-
ogy of predefined species and populations. They all include
physiological databases that are combined with compound-
Figure 1 (a) Representation of the generic structure of a whole-body PBPK model. (b) Hierarchical representation of the main physio-
logical and drug parameters in a PBPK model. (c) Simulation of drug concentrations in different tissues using different distribution mod-
els for theophylline. This illustrates the impact of the choice of the distribution model on the simulated tissue concentration profiles
even though corresponding plasma concentrations are very similar. (d) Example of relative gene expression data for a group of
enzymes (in healthy and cancer patients), receptors, and transporters. Gene expression is represented as relative value obtained
through normalization to the tissue or organ with the highest expression.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

specific information as well as biometric data, and are used
to parametrize a PBPK model on a whole-body level.
In previously published tutorials, Jones and Rowland-Yeo4
introduced some of the basic concepts of PBPK as well as
the use of PBPK in drug discovery and development, while
Maharaj and Edginton5 described the use of PBPK in pediat-
ric clinical development. The aim of this tutorial is to cover
the fundamental concepts of PBPK/PD models, focusing on
their practical implementation in a typical PBPK model build-
ing workflow. In the next sections an overview of the infor-
mation contained in the different building blocks of the model
(section “Building blocks in PBPK modeling”) will be pre-
sented and then the different parameters included in the
model structure will be discussed in more detail (section
“Passive and active processes”). Finally, practical guidance
on the different steps of the model-building process will be
provided (section “Best practices in PBPK model building”)
and an example of PBPK/PD model will be discussed (sec-
tion “Case study: Building a PBPK model for ciprofloxacin”).
Applications of PBPK modeling
Computational models provide an ideal platform for knowl-
edge management since they offer the opportunity to collect,
integrate, analyze, and store information. Ideally, in an
integrative and iterative workflow such models can be used to
generate working hypotheses from simulations. In turn, these
hypotheses can then be tested in specifically designed
experiments that may lead to a better understanding of the
underlying processes and a refinement of the model. In the
case of pharmaceutical applications, the main goals of PBPK
modeling include (Figure 3): generating and testing a mecha-
nistic understanding of the physiological processes that gov-
ern an observed drug behavior; translating the understanding
to novel settings (e.g., to a different population); identifying an
ideal therapeutic regimen; and optimizing risk–benefit ratios.
In fact, any deviation between the model simulation and the
data can provide insights into the mechanisms of the underly-
ing processes that may not yet be reflected in the existing
model.
Another
important
application
of
PBPK
models
are
extrapolations to novel clinical scenarios such as different
treatment schedules or patient subgroups. Notably, transla-
tion to novel therapeutic designs can usually be achieved
by only changing single or limited sets of parameters.
Extrapolations to different species or specific populations,
in contrast, require knowledge of the sets of parameters
characterizing the physiological properties of the species or
particular patient cohort of interest.6
Figure 2 Representation of the general building blocks which can be part of a PBPK model. Some components may be optional
depending on the model considered.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License Typical applications of PBPK modeling include but are
not limited to:
• Pediatric extrapolations,5,7 where, with the support of the
US Food and Drug Administration, a reference PBPK
model for an adult population is scaled to specific life
stages in children.
• Extrapolations to diseased populations, e.g., hepatically
impaired cirrhotic patients.8
• Evaluating the effect of possible drug–drug interactions
(DDI), e.g., by considering competitive inhibition of a
metabolizing enzyme.9
• Scaling between different treatments scenarios by simu-
lating specific dosing schemes.10
• Assessing the impact of different drug formulations by
modifying
corresponding
compound/formulation
parameters.11
Advanced applications include cross-species extrapola-
tion,12,13 multiscale modeling,14–16 and statistical modeling
using methods such as Bayesian approaches.17
Pharmacodynamic modeling
PBPK models offer a mechanistic framework to quantify the
pharmacodynamic (PD) effect of a drug through coupling to
simulated on- and off-target tissue concentrations. The final
result in this case would be a PBPK/PD model. An example
of such a model is discussed in the ciprofloxacin case
study presented in section “Case study: Building a PBPK
model for ciprofloxacin” of this tutorial. Since different
organs are explicitly represented in PBPK models, on- and
off-target tissue exposure can be directly quantified. This
enables a consideration of therapeutic or toxic effects by
coupling of PD to the corresponding PBPK models. To this
end, tissue concentration profiles simulated with PBPK
models may be used as input for downstream PD models.
Notably, this coupling of PK and PD results in a multiscale
PBPK/PD model that simultaneously describes drug ADME
at the whole-body level and the resulting drug effect at the
cellular or tissue scale.
In the simplest case, PD models may represent simple pro-
liferation models quantifying, for example, bacterial growth in
infection biology18 or tumor growth in oncology.19 Given the
ever-growing number of systems biology models at different
scales of biological organization, the PD disease or toxicity
models may be largely expanded. Examples of such detailed
PBPK-based models include glucose-insulin regulation in dia-
betes,10 management of endometriosis,20 acetaminophen
intoxication,15 drug-induced liver, injury21 or model-based
design and analysis of antithrombotic therapies.22 Ultimately,
such PBPK/PD models aim for a mechanistic and physiologi-
cal representation of systems interactions within the body,23
thereby providing an important toolbox for disease or toxicity
modeling in quantitative systems pharmacology.
Figure 3 Schematic representation of the most common applications of PBPK modeling.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License BUILDING BLOCKS IN PBPK MODELING
Anatomy and physiology
The physiology of the organism of interest is essential prior
knowledge in PBPK modeling and relevant organs are
explicitly included in the model. Each organ is represented
by its anatomical and physiological properties; for example,
volume, tissue composition, and perfusion blood flow rates.
Furthermore, in some cases each compartment can be fur-
ther divided into subcompartments, such as plasma, inter-
stitium, cellular space, and red blood cells. Structurally,
these subcompartments are the lowest level of structural
differentiation in PBPK models and, for example, enzymatic
processes can be localized in the relevant intracellular com-
partment to which the extracellular space can be connected
by passive diffusion and additionally by active drug trans-
port, where required. Without subcompartmentalization cer-
tain effects such as permeation limited metabolization
within the liver may not be represented. Blood flow governs
mass transfer within the body, and its rate is specific to each
organ.
Where
necessary,
a
more
detailed
mechanistic
description of a subset of organs can be included in the
model; for instance, to obtain a more accurate description of
the distribution in the brain,24 liver,25 kidney,26,27 or lung,28 or
describe in detail the process of intestinal absorption.29–31
Generally, two blood compartments, arterial and venous
blood, connect the organ compartments in a PBPK model.
Yet in clinical practice it is common to sample blood only
from the superficial veins of patients, e.g., the antecubital
vein. Thus, the measurements collected in peripheral veins
present a concentration that may differ significantly from
both arterial and central vein compartments, making the
comparison of model predictions with collected data diffi-
cult. To solve this discrepancy, Levitt32 proposed a model in
which an additional organ representing the tissues drained
by the antecubital vein was added such that the concentra-
tion in the peripheral venous blood can be described.
Based on this model, a peripheral venous blood compart-
ment has also been included in some PBPK software
tools.12,33
Gastrointestinal transit and absorption models. For an orally
administered drug, a combination of physiological, com-
pound, and formulation-related aspects comes into play.
These affect the relevant parameters such as solubility, dis-
solution rate, and intestinal permeability.
From a general perspective, the gastrointestinal (GI) tract
can be divided into several segments based on their ana-
tomical and functional role: stomach, small intestine (duo-
denum, upper and lower jejunum, upper and lower ileum)
and large intestine (cecum, colon ascendens, colon trans-
versum, colon descendens, sigmoid, and rectum). Each of
these segments can be further divided into zones repre-
senting the lumen and gut wall, which can in turn be divid-
ed into mucosal and nonmucosal tissues. The separation of
the mucosal tissue from the remaining part of the gut wall
allows the absorption processes to be described in a realis-
tic manner, reflecting the localization of active processes
such as gut wall metabolism in the respective tissue.34
After oral administration, the drug is transported along
the lumen of the intestine according to a transit function. It
can enter the mucosa of the corresponding segment either
by the transcellular route (passing via the enterocytes into
the intracellular space) or by paracellular diffusion into the
interstitial space of the mucosa. The paracellular route has
been shown to contribute significantly to the overall intesti-
nal absorption of a few small molecules such as acyclovir,
cimetidine, and ranitidine.29 However, the paracellular route
is in general considered to contribute only marginally to the
intestinal absorption, mainly due to the small surface area
fraction that allows paracellular permeation.35 During the
transit through the lumen, the maximum concentration of
the drug might be limited by the local pH-dependent GI sol-
ubility, which can be calculated using the Henderson–
Hasselbalch equation. The intestinal pH will also affect the
degree of dissociation of the compound, and consequently
the relative concentration of neutral vs. the charged form(s).
In this case, the charged molecules have a lower perme-
ability than the neutral form, and this should be also
accounted for in the model.36
Drug properties
The second major type of input into PBPK models are
compound-specific parameters. These include the physico-
chemical parameters of the compound (e.g., MW, lipophilic-
ity,
solubility,
and
pKa
values)
that
can
usually
be
determined in vitro. Lipophilicity is a key parameter that,
together with the MW, is used to calculate the membrane
permeability of a drug. The MW is, in this context, a surro-
gate measure for the size of the molecule. Since halogen
atoms in particular contribute less to the molecular volume
than expected from their atomic weight, a correction term
can be applied to obtain an effective MW, which is a better
representation of the size.36 Particularly relevant for oral
administration, drug solubility determines the availability for
absorption of a compound in the GI tract, while pKa values
are used to calculate pH-dependent changes in drug solubili-
ty. Pharmacokinetic parameters, such as fraction unbound,
are likewise compound-specific, yet they also depend on the
organism. These basic values are frequently used together
with physiological parameters to calculate other parameters
that are much more difficult to measure but can be used
immediately to quantify the drug mass balance in PBPK
models. For example, tissue–plasma partition coefficients
quantifying the distribution of a compound are calculated
from MW, lipophilicity, fraction unbound, and pKa values,
depending on the distribution model used (see below). Frac-
tion unbound, the fraction of a drug not bound to plasma
proteins, strongly influences drug distribution and clearance
since only the available free fraction of a compound diffuses
into cells, where it might be metabolized. Also, only the free
fraction of a compound is filtered for renal excretion. The
fraction unbound can either be measured experimentally,
estimated from the drug concentration, or predicted from the
lipophilicity of the drug, respectively.37 Notably, all the afore-
mentioned compound-specific parameters contribute to the
quantification of passive processes such as membrane per-
meation and organ/plasma partitioning. On the other hand,
key parameters for quantifying active processes such as
enzymatic activity (Vmax) must be obtained by a comple-
mentary approach. For example, parameters for an active

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License process can be determined in vitro or fitted from in vivo data
and then converted to the enzymatic rate or a different
parameter.
Formulation
The development of oral dosage forms for new chemical
entities is often the favored option in drug development.
The design and development of such formulations can be
supported by accurate mechanistic models that can simu-
late in vivo bioavailability. In vitro dissolution profiles in bio-
relevant
media,
such
as
the
Fasted
State
Simulated
Intestinal Fluid (FaSSIF) and the Fed State Simulated
Intestinal Fluid (FeSSIF), have been established. When
used in standardized in vitro dissolution test methods, such
media allow simulating the in vivo disintegration and disso-
lution behavior of orally administered dosage forms.38 This
dissolution profiles together with drug PK profiles can be
used to establish an in vitro–in vivo correlation (IVIVC).
Such correlation enables the estimation of in vivo concen-
tration PK profiles from the in vitro dissolution profiles of dif-
ferent formulations, providing a tool for optimizing the
administered dosage form with a minimal number of in vivo
animal experiments or clinical trials.39
As an alternative to a direct correlation between in vitro
and in vivo concentrations, it is possible to include dissolu-
tion functions in the GI compartments of PBPK models to
account for the disintegration and dissolution processes in
the GI tract.40 The inclusion of such dissolution profiles in
GI physiological models and their combination with whole-
body PBPK models has been described in the literature.30
Routes of administration and administration protocols
The administration protocol includes the (1) route of admin-
istration, (2) amount of compound (dose), and (3) an
administration scheme for multiple dosing. Usually, when
comparing model simulation to available data, the adminis-
tration protocol used in the model will match the one used
in the study for which the data are under evaluation.
Various routes of administration can be considered in the
model. This will define how the drug is absorbed and, part-
ly, how it will be distributed in the body. Common adminis-
tration
routes
are
intravenous
(i.v.)
and
oral
(p.o.)
administration, but also alternative routes such as inhala-
tion, subcutaneous, intramuscular, topical, or ocular admin-
istration are used in PBPK models. Apart from i.v., when
considering other administration routes, also mechanistic
consideration related to local drug release and absorption
from the administration site should be included in the PBPK
model,
for
instance
to
describe
the
progressive
release and diffusion from the injection site after intramus-
cular administration.
PASSIVE AND ACTIVE PROCESSES
In PBPK modeling, physiological parameters provide the
structural scaffold of the model, but active and passive pro-
cesses describe the actual distribution, excretion, and
metabolization of the drug (mass balance). The most
important passive processes are tissue permeation and
organ/plasma partitioning. The underlying processes are
calculated from substance-specific surrogate markers, such
as lipophilicity, to obtain, for example, permeability or parti-
tion coefficients. Different concepts for quantifying passive
and active transport processes are described in the follow-
ing sections.
Estimation of passive processes from physicochemical
properties for small molecules
Distribution models. Small molecules can generally pene-
trate all kinds of tissues in the body. Experimentally, the
quantification of this compound-specific distribution is very
labor-intensive.41,42 A major advance in PBPK modeling
came with the use of calculation methods for organ/plasma
partition coefficients, which describe steady-state ratios of
the concentrations in the blood or plasma and the sur-
rounding tissue. Various concepts for mechanistic correla-
tions have been developed for the in silico estimation of
organ/plasma partition coefficients. Based on tissue compo-
sition, these coefficients can account for the distribution
between drug-binding tissue constituents, such as proteins
or lipids, on the one hand, and water on the other. Although
the principles are very similar in all cases, the calculation
methods deviate with respect to the kind of parameters
used and resulting in different values of tissue concentra-
tion (Figure 1c). All known partition coefficient models
assume that tissue is composed of a limited number of
components, and they all include partition coefficients for
water/protein and lipid/water. These two partition coeffi-
cients are usually calculated from so-called surrogate in
vitro measurements. The total organ/plasma partition coeffi-
cient is then calculated as a weighted sum of the partition
coefficients for all of the components; the weights are the
volume fractions of each component. Importantly, the distri-
bution of a drug within aqueous and organic tissue compo-
nents is always assumed to be homogenous and passive.
The most widely used concepts for calculating organ/
plasma partition are briefly introduced below:
• Poulin et al.43,44 calculate the lipo-hydrophilicity of tissue
as a mixture of neutral lipids, phospholipids, and water. In
addition to the volumetric tissue composition, fraction
unbound (fu), lipophilicity (logP and logD), and pKa are
used as compound-specific input parameters. Here as
well as in all the following concepts for the calculation of
organ/plasma partition coefficients, fu quantifies specific
reversible binding to proteins in plasma and tissue,
whereas lipophilicity accounts for nonspecific binding to
lipids.
• Rodgers et al. extended the concepts of Poulin et al. to
electrostatic interactions at physiological pH.45,46 These
include binding of ionized and unionized drugs to acidic
phospholipids and neutral lipids, respectively. Also elec-
trostatic drug interactions with extracellular proteins are
taken into account. Consequently, the partition coeffi-
cients are calculated taking into account the lipophilicity
and pKa value of the drug and the pH values of the
tissues.
• Berezhkovskiy47 modified the calculation method by Pou-
lin et al. by accounting for peripheral drug elimination that
results in a different volume of distribution.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License • Willmann et al.48,49 extended the concept of Poulin et al.
by additionally considering proteins as a tissue compo-
nent. Moreover, Willmann et al. use membrane affinity
(logMA)50 to quantify partitioning between water and an
artificial cellular membrane as a measure for lipophilicity
by using an empirical equation.51 This model is imple-
mented in the PK-Sim software as the PK-Sim standard
distribution model.
• Schmitt52 developed a method for calculating the organ/
plasma partition coefficient for organic compounds, by
compartmentalizing tissue as water, neutral lipids, neutral
phospholipids, acidic phospholipids, and proteins. This
concept accounts in particular for electrostatic interac-
tions between charged molecules at physiological pH and
acidic phospholipids. Also for this distribution method, the
partition coefficients are calculated taking into account
the lipophilicity and pKa value of the drug and the pH val-
ues of the tissues.
As shown in Figure 1c, different distribution models can
be used to describe similar plasma concentration profiles of
the drug but, because of the intrinsic nature of the models,
they will generate different tissue concentrations. If tissue
concentrations for the drug are not collected, when assess-
ing target site drug exposure it should be kept in mind that
the selection of the distribution model represents a funda-
mental assumption during model development. An inherent
uncertainty should hence be taken into account in the pre-
dictions. Ideally, different distribution models should be
available during model development to allow for full struc-
tural flexibility in this regard. It should be kept in mind that
Figure 1c represents a specific example for the theophyl-
line molecule, and it should not be used to draw any con-
clusion concerning comparison of distribution models and
tissue predictions since the simulated concentrations are
largely dependent on the drug parameters used as input.
Permeability models. Diffusion across the vascular wall
from plasma to interstitial space of the organs or diffusion
across the cellular membranes of tissue cells or red blood
cells determines how fast drug distribution takes place and
can be rate limiting for distribution (permeation limited kinet-
ics). In general, the diffusion across the vascular wall is
assumed to be fast for small molecules. However, this
assumption might not hold true for drugs with high protein
binding or which are highly hydrophilic.53 Also in the case
of large molecules (e.g., protein therapeutics) this assump-
tion does not hold true (cf. section “Passive and active pro-
cess for large molecules”).
The cellular membrane is the diffusion barrier between
interstitial space and intracellular space or between blood
plasma and blood cells. The rate constant describing the
diffusion across the cellular membrane can be written as
the product of the drug permeability (P) and the effective
surface area (SA) of the cells. Methods to calculate the
drug-specific permeability depending on physicochemical
properties like lipophilicity and MW can be found in the liter-
ature.54,55 In order to calculate the effective surface area
for different organ volumes, allometric scaling equations
can be used.56
An important consideration in calculating the rate and
extent of intestinal drug absorption is the intestinal perme-
ability. There are several experimental techniques that are
able to provide a relatively reasonable assessment of the
intestinal permeability, e.g., artificial membranes,57 “intestine-
like” cell lines (e.g., Caco-2 or MDK),58,59 Ussing chambers,60
and in situ rat intestinal perfusion techniques (e.g., single-
pass intestinal perfusion).61 In humans, effective permeability
in different regions of the intestine can be measured using
single-pass perfusion methods.35 An alternative approach for
establishing the intestinal permeability is to use the physico-
chemical properties as a basis for calculations.1 Several
models are available for this approach; for instance, the mem-
brane affinity of a compound (defined as its equilibrium parti-
tion coefficient for water and immobilized lipid bilayers) and its
effective MW can be used for such calculations, using a semi-
empirical equation.51
Estimation of active processes for small molecules
Active processes allow the inclusion of additional mechanis-
tic details in PBPK models, since they can frequently be
assigned to biochemical processes at the molecular scale.
Examples of such processes are metabolization reactions,
in which a molecule is transformed and modified, as well as
transport processes, in which a compound is actively taken
up or secreted into a specific tissue compartment. Quantifi-
cation of active processes follows different concepts than
the ones of passive processes, relying on either careful
extrapolation of in vitro results to an in vivo situation or
knowledge-based adjustment of parameters that are difficult
to measure experimentally. In general, all clearance pro-
cesses presented can be formulated as, for, instance first-
order clearance kinetics or Michaelis–Menten kinetics. The
Michaelis–Menten kinetics are often used to describe pro-
cesses that can be saturated by the substrate concentra-
tions; its equation is the following, with v representing the
reaction rate, Vmax the maximum reaction rate, Km being
the Michaelis–Menten constant and the substrate concen-
tration [S]:
v5 Vmax  ½S
Km1½S
(1)
If [S] is significantly lower than Km, elimination kinetics can
be considered linear (first-order process) and the rate con-
stant for the clearance process can be approximated by the
ratio Vmax/Km.
Parameters included for active processes are typically
rate constants for elimination or active transport processes
(e.g., intrinsic hepatic clearance, Michaelis–Menten param-
eters Km and Vmax, or parameters describing specific bind-
ing, for instance, to a receptor kon and koff). Examples of
such processes are metabolic elimination related to a par-
ticular enzyme, or transporter activity or drug distribution
due to binding partners. Parameters that define active pro-
cesses are usually extrapolated based on in vitro measure-
ments,62,63 when the necessary extrapolation factors for
measurement settings are available, or fitted using in vivo
data.64 In vitro–in vivo extrapolation (IVIVE) can be applied

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License to the different stages of absorption, distribution, metabo-
lism, and excretion (ADME) processes.
Intrinsic and total plasma clearance. Clearance is generally
used to quantify elimination rates in liver, kidney, or other
organs. At the body level, total plasma clearance (CLtot, i.e.,
volume of plasma cleared per time unit) describes the sum
of multiple clearance processes that occur simultaneously
within multiple organs. Here, CLtot is the apparent rate at
which a compound is removed from the systemic circulation.
In PBPK modeling, the relative contribution of each organ to
CLtot can be further differentiated by quantifying the specific
elimination rate in each organ. In this case, the intrinsic
clearance CLint is used to quantify the intracellular activity of
a metabolizing enzyme in different organs.65
In vitro–in vivo extrapolation of clearance. For liver clear-
ance, numerous in vitro assays are available to estimate
the enzymatic activity, and this clearance needs to be
rescaled to the whole-organ in vivo situation. For example,
activity can be derived from recombinant cytochromes,
human hepatocytes, or human liver microsomes. For an
IVIVE, the experimentally measured specific activity needs
to be multiplied by the amount of catalyzing agent (amount
of cytochrome, number of hepatocytes, or amount of micro-
somal protein) per gram of liver tissue to obtain the specific
intrinsic clearance per gram of liver. The ratio of Vmax/Km
describes the intrinsic metabolic clearance for unsaturated
conditions, which can be derived from in vitro studies in
human liver microsomes. In the past, IVIVE was routinely
conducted based on mean data disregarding interindividual
variability. As an alternative approach, it has been proposed
to estimate enzyme abundance and its variability, measured
by immunoquantification, to allow a direct extrapolation to
the population level.66,67
The second main clearance route in the body is usually
renal secretion. Total renal clearance can be derived from
the fraction of a drug secreted in the urine. This value can
be further differentiated into glomerular filtration, which
describes the passive filtration rate of urine in the kidney,
and tubular reabsorption and tubular secretion, which are
driven mainly by active transport.
Protein abundance in active processes. Although the liver
and kidney are the key secretory organs of the body, the
expression of many enzymes and drug transporters is not
limited to these two organs. One way to quantify the contri-
bution of different organs to the total clearance at the
whole-body level is to consider the relative tissue-specific
expression
of
genes
or
proteins.
Recently,
a
generic
approach was proposed whereby gene expression is used
as a surrogate for tissue-specific protein abundance in
PBPK modeling.3,12 The catalytic activity of each process is
generally quantified for each organ by Vmax (lmol/l/min).
Notably, Vmaxj is the product of the catalytic efficiency kcat
(1/min) and the overall concentration of the catalyzing pro-
tein E0,j (lmol/l) in the corresponding organ j:
Vmaxj5kcat  E0;j5kcat  E0  erel;j5kcat  erel;j
(2)
This
reformulation
allows
describing
the
tissue-specific
abundance of an enzyme or transporter (E0,j) as the prod-
uct of its overall concentration, Eo, and its relative expres-
sion, erel,j, in a specific organ j. While Eo is obviously not
accessible experimentally, relative expression profiles (erel,j)
across different tissues may be obtained from public data-
bases.3 In the above equation, kcat* is a new parameter
that combines the catalytic efficiency kcat and the overall
concentration Eo. This parameter needs to be estimated
through parameter optimization. Moreover, it should be not-
ed that this reformulation reduces significantly the number
of independent model parameters, since only a single
parameter
(kcat*)
needs
to
be
considered
instead
of
assigning a catalytic efficiency Vmaxj separately for each
organ. Please note also that the relative tissue-specific
abundance of an enzyme or a transporter may be approxi-
mated either through gene or protein expression, respec-
tively,3 even though correlations of both are a matter of
debate. This is because any posttranscriptional effect can
be assumed to be largely protein specific, as such only
impacting kcat*. The use of expression data to quantify
relative tissue-specific catalytic efficiency represents a com-
plementary approach to the IVIVE of clearance process-
es.68 Likewise, drug elimination in first-pass organs such as
liver, lung, or GI as well as other organs can be described.
Figure 1d shows the relative gene expression for a
group of enzymes, receptors, and transporters in healthy
individuals or cancer patients, respectively. Note that the
relative expression is dimensionless following normalization
to the tissue with the highest expression. As expected,
cytochrome P450 expression is consistently largest in the
liver and the intestines, while receptor expression is rather
ubiquitous. In turn, transporter availability is similar to cyto-
chrome P450 with an occasional small contribution in the
kidney (MRP2, BCRP). Interestingly, CYP2D6 expression is
higher in the large intestine than in the liver in two indepen-
dent measurements (healthy subjects and cancer patients).
To validate this observation protein expression data from
the literature could be alternatively used for model building,
instead. Only a limited number of organs or tissues are rep-
resented for illustration.
Receptor availability. The above-described concepts use
expression data to quantify catalytic efficiency but they are
applicable to both enzymatic processes and drug transport-
ers as well. Notably, the approach can immediately also be
applied to estimate the abundance of receptors for different
drugs,
including
antibody-drug
conjugates.69
Thus,
the
availability of specific drug binding partners can be quanti-
fied simultaneously in multiple organs; this has enormous
potential for mechanistic consideration of target-mediated
drug disposition or clearance, as well as on/off-target
effects.
Passive and active processes for large molecules
Therapeutic proteins are an increasingly important class of
drugs.70 PK/PD modeling of therapeutic proteins differs
from those of small-molecule drugs, mainly due to the dif-
ferences in size.71–73 PBPK models as well must therefore

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License take into account the special mechanisms that govern the
pharmacokinetics of protein therapeutics, mechanisms that
can often be neglected for small molecules. Both the
exchange of drug across the vascular endothelium and the
return of drug by the lymph flow from the interstitial space
of the organs to the systemic circulation are important phe-
nomena for therapeutic proteins. These two processes
influence the volume of distribution for proteins, and are
generally
considered
in
PBPK
models
of
therapeutic
proteins.74–84
Published PBPK models use various approaches to
describe the extravasation of protein therapeutics. One
commonly used is the two-pore formalism,85,86 which con-
siders the barrier between the plasma and the interstitial
space as a membrane consisting of two types of pores: few
large ones and many small ones. Macromolecules are
assumed passing through these pores by convection as
well as by diffusion; convection being the predominant
extravasation mechanism for large protein therapeutics
such as antibodies or albumin.
Another relevant process for antibodies or other proteins
(e.g., albumin fusion proteins) is the catabolism within
endosomal space and the protection from catabolism by
neonatal Fc receptor (FcRn), which is also often taken into
account by more recently published PBPK models.76–84
In describing the lysosomal degradation of drugs and
their recycling by FcRn, the organ representation used for
small molecules is usually extended by adding a compart-
ment for the endosomal space. This space represents the
region within the endothelial capillary walls where catabo-
lism and high-affinity binding to the FcRn occurs (acidic
environment). The fraction of drug that is bound to FcRn is
recycled to the plasma and interstitial space, whereas the
unbound fraction is subject to endosomal clearance. Addi-
tional processes can also be important and implemented if
needed. Examples include target-mediated disposition and
clearance84 and immunogenicity.87,88
BEST PRACTICES FOR PBPK MODEL BUILDING
Due to increasing application of PBPK modeling in drug
development and regulatory submissions, there have been
recent efforts by regulatory agencies, industry, and aca-
demia to discuss and develop best practices for establish-
ing as well as reporting of PBPK modeling.89–94 In this
section, general recommendations for PBPK model building
are provided (for information specific to applications for
pediatric populations, see Refs. 5,95).
Compilation of available data and information
As a first step in model development, all available informa-
tion on the drug regarding its ADME properties are gath-
ered. This includes the drug-specific parameters, which are
used as input parameters, and the characterization of the
organism or population. Default physiological parameters
should only be changed if there is a mechanistic rationale,
for instance, in the case of special populations. The physi-
cochemical drug properties (see section “Drug properties”)
are necessary parameters to inform the drug distribution.
Besides these parameters, any further ADME information
regarding, for instance, clearance processes, transporters,
or specific binding partners are relevant in order to build
physiologically plausible models. The appropriate level of
detail in representing the relevant processes and the crite-
ria for model evaluation depend on the particular aims,
objectives, and applications of the model as well as on
availability of data and information. Available experimental
PK data are used to identify unknown or uncertain parame-
ters as well as for model validation. Depending on their
availability, data commonly used in PBPK model building
includes time–concentration profiles of the drug in the plas-
ma (for different preclinical species and/or humans, differ-
ent application routes, different dosages, or applications
schemes), time–concentration profiles of the drug in rele-
vant tissues, the percentages of drug excreted via the urine
and feces, mass balance data, and metabolites data (time–
concentration profiles, excretion data). A scheme of the
PBPK model-building workflow for small molecule drugs is
provided in Figure 4.
Establishment of the PBPK model for i.v.
As a first step, a method for calculation of organ/plasma
partition coefficients, frequently referred to as distribution
model, needs to be chosen to describe the drug distribution
behavior. The distribution model selected for a certain com-
pound should be able to consistently describe the com-
pound distribution independently of the considered species
or administration protocol. By comparing simulations with
PK measurements in vivo after i.v. administration, different
distribution models can be compared and clearance param-
eters can be estimated. The clearance parameters can be
estimated from experimental in vivo data, i.e., plasma
concentration–time profiles. Additionally, mass balance data
might be used if different elimination pathways should be
informed. Rates for metabolism processes might also be
estimated using IVIVE approaches (see section “In vitro–in
vivo
extrapolation
of
clearance”).
Surrogate
compound
parameters, like lipophilicity, are usually slightly adapted at
this stage to obtain a good agreement with experimental
i.v. data. There are no established rules regarding the
extent
of
change
that
is
reasonable,
since
this
also
depends on which lipophilicity measure is used as starting
value. Even though a PBPK model may comprise several
hundreds of ordinary differential equations, the number of
independent model parameters for a new compound is usu-
ally small (in most cases, fewer than five per compound),
due to the large amount of prior, independent physiological
information that is incorporated (Figure 1b). As in the case
of the distribution models, also these compound-specific
parameters are usually kept unchanged across different
species or administration protocols. If the selection of distri-
bution models and adjustment of parameters are not suffi-
cient to describe the i.v. data, this can be an indication that
relevant processes are not yet taken into account in the
model. In such cases, for instance, active transport or bind-
ing partners can be incorporated based on current knowl-
edge or as testable hypothesis. Such additional processes
might also be needed to explain features such as dose

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License nonlinearity, the observed extent of clearance, or the drug
distribution. When introducing additional processes, it is
best to include as much experimental data as possible
(e.g., Km and Kd, values, abundance of enzyme, binding
partner). It should be noted that data for different doses
have to be available (showing dose-nonlinearity) in order to
be able to identify Michaelis-Menten parameters, e.g., for
transporters or clearances.
Establishment of the PBPK model for oral
Once an i.v. model is established, a model for p.o. adminis-
tration (or for other extravascular routes) can be estab-
lished. In this step none of the parameters that influence
distribution or metabolism/excretion should be further modi-
fied and only those parameters that influence the oral
absorption should be varied. Typical parameters to be esti-
mated during development of a p.o. model are intestinal
permeability and parameters related to meal events. In
addition, formulation-related parameters describing drug
release as well as solubility might be adjusted, especially if
aqueous solubility rather than FaSSIF and FeSSIF solubility
were
used
as
starting
values.
After
that,
additional
absorption-related processes, such as enterohepatic recy-
cling (EHC), might be included if relevant for the drug under
consideration. The stepwise approach of i.v. and p.o. (or
any extravascular administration) model building is described
to stress that during the establishment of a model including
Figure 4 Flowchart illustrating the steps usually used in PBPK model building.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License drug absorption, the information regarding distribution and
clearance processes from the i.v. data should be used in
order to be able to identify the parameters relevant for
absorption. Note that in some cases the proposed strictly con-
secutive building of i.v. and p.o. PBPK might not be the best
approach; for instance, if the i.v. model incorporates process-
es that are also relevant for oral absorption, e.g., uptake
transporters. In such cases, it might be preferable to perform
parameter
identification
using
the
i.v.
and
p.o.
data
simultaneously.
As mentioned, i.v. data are highly valuable, since they
allow informing distribution and clearance processes inde-
pendent from the drug absorption. Depending on the
modeling purpose and the needed model precision, a
PBPK model might also be developed using p.o. data only.
Taking into account data on drug absorption, metabolism,
and mass balance data, it is necessary to rely on the
PBPK or IVIVE methods regarding prediction of absorption
or clearance. If human i.v. data are missing, a human p.o.
model might be scaled from an animal model that was
established using i.v. as well as p.o. data. Without using i.v.
data, the model uncertainty can be considerably higher
depending on the BCS classification of the drug and if
transporters or gut-wall metabolism are involved.
Overall model evaluation
After model development, the model quality should be eval-
uated. This step should address whether the model fits its
purpose. As such, the outcome of the evaluation depends
on the goal of the modeling project. The following criteria or
tests can be used in evaluating the model.
Agreement of modeling outcome with experimental data.
Usually, a model is evaluated by visually comparing simu-
lated vs. experimental concentration–time profiles (for plas-
ma and, if available, for other tissues), focusing on the
absolute concentrations and the dynamic shape of the PK
profile or by means of error functions such as root-mean-
square deviation (RMSD), the area under the curve (AUC)
error,12 or the concordance correlation coefficient.16 Addi-
tionally, typical PK parameters like Cmax, tmax, AUC, and t1/2
can be compared between data and simulation during mod-
el evaluation. While comparing model simulations and
experimental data, it should be considered that both are
subject to uncertainty, and also experimental data might be
critically reevaluated. In addition to data used for model
building, further data can also be considered as external
validation to assess consistency of model prediction.
Consistency of PBPK models for different doses, across
species, special populations, and compounds. An important
cross-check for model validation is the consideration of dif-
ferent doses. Deviations in estimations for dose levels that
had not been considered during model development point
to
structural
shortcomings
of
the
model.
The
drug-
dependent parameters as well as the calculation methods
for distribution and cellular permeability should be the same
across all species for a certain drug. If this is not possible,
a plausible physiological explanation, as, for
instance,
species-specific processes, should be discussed. If PK
data for special populations, such as hepatically or renally
impaired patients, are available, the model can also be
evaluated using these data after changing the physiological
parameters accordingly. The model might additionally be
evaluated for consistency across compounds for which the
same processes are relevant for the ADME properties. For
example, if a saturable receptor binding was implemented
as a relevant process into a PBPK model, it could be
checked if the receptor concentration is the same in a
PBPK model of a reference compound binding to the same
receptor.
Sensitivity analysis or best- and worst-case scenarios. In
order to assess uncertainties in model results, it is recom-
mended to perform a sensitivity analysis for relevant param-
eters.
Such
sensitivity
analysis
can
be
performed,
for
instance, on uncertain parameters for active processes
included in the PBPK model or to all parameters in the mod-
el, in order to identify the most sensitive parameters for a
specified model output (e.g., plasma concentration or PK
parameters). Additionally best- and worst-case scenarios
can be simulated in order to evaluate the effect of changing
uncertain parameters to extreme values within the experi-
mental and physiological uncertainties. Uncertainties regard-
ing underlying mechanisms can be assessed by simulating
the respective model alternatives. The results of the sensitiv-
ity analysis or best- and worst-case scenarios can be used
to assess if the conclusions of modeling work are robust.
CASE STUDY: DEVELOPING A PBPK/PD MODEL FOR
CIPROFLOXACIN
In order to illustrate the various steps of PBPK model
development in a practical example, the construction of a
PBPK model for the antibiotic ciprofloxacin (CIP) will be
described in this section. Following the best-practices sec-
tion above, the experimental data needed for parametriza-
tion of the basic model structure will be discussed and it
will be shown how both i.v. and p.o. administration of the
drug may be systematically considered during model estab-
lishment. Finally, an empirical PD model of CIP treatment
of E. coli infections18 will be coupled to the PBPK model.
This resulting PBPK/PD model will be then used to simulate
the therapeutic effect of different dosing schemes. The indi-
vidual steps in model development are provided as a
hands-on tutorial in the Supplementary Materials. The
final modeling example shows prototypical demands and
applications of PBPK modeling in a pharmaceutical devel-
opment program.
The first step in PBPK model building is gathering and
assembling existing information. In this regard, the basic
physicochemistry of the drug is of particular importance
(Table 1A). The physicochemical information in Table 1A
can be plugged directly into a PBPK software tool, where it
is used to calculate all indirect PBPK model parameters
from the models, as explained above. Notably, the informa-
tion provided in Table 1A, together with the exhaustive col-
lections of physiological parameters integrated in PBPK
software tools, is sufficient to obtain a preliminary, yet fully

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License parametrized initial model regarding absorption and distri-
bution processes.
In the case of CIP, various clinical studies have been per-
formed to identify physiological processes governing drug
ADME. The following assumptions were made in the model:
(1) CIP is metabolized via CYP1A2,96 (2) CIP is secreted
into bile ducts in the liver,97 and (3) CIP is subject to signifi-
cant renal elimination.98 In this regard, it is interesting to
note that the rate at which CIP is excreted in the kidney can-
not be explained by passive glomerular filtration alone; active
tubular secretion must also contribute to the excretion pro-
cess. In the case of a novel compound, the parametrization
of such active physiological processes requires either IVIVE
of physiological parameters in combination with dedicated
scaling factors68 or identification of the model parameter
using targeted experimental mass balance and excretion
data. For the CIP example discussed here, it was assumed
that the contribution of each of the three above-mentioned
physiological
processes
has
been
determined
before
(Table 1B). Because CIP demonstrates dose linear PK,99 all
three processes are quantified by first-order kinetics.
Assuming a mean standard individual (i.e., an individual
with average demographic covariates) and a given administra-
tion scheme, the resulting PBPK model can be used for a first
simulation of drug plasma concentrations. As outlined in the
best-practice section above, the establishment of a PBPK
model for an i.v. administration is usually a reasonable first
step, since it makes it possible to ignore all effects related to
absorption in the GI tract. Here, clinical data for i.v. administra-
tion of 200 mg CIP are considered.100 For initial PBPK model
building, the physicochemical properties of CIP (Table 1A)
are first integrated into the PBPK software to calculate the
basic distribution model. In a second step, parameters for
physiological metabolization and excretion processes were
estimated from experimental PK data (Table 1B). Whereas
renal excretion and biliary secretion are solely linked to single
organs, i.e., kidney and liver, respectively, enzyme-mediated
metabolization may simultaneously occur in tissues through-
out the body. For the CIP model, relative CYP1A2 abundance
was quantified, using tissue-specific gene expression as a sur-
rogate for protein availability3 (Figure 1d). In the resulting
PBPK model, the distribution, metabolization, and excretion of
CIP is structurally represented. The standard distribution of
PK-Sim was identified as the most accurate distribution mod-
el, and the associated model parameters are quantified. Since
the main focus is on intravenous administration during initial
establishment of the model, as mentioned, it is reasonable to
ignore oral absorption at this time. Note that a mean patient is
usually represented by the collection of physiological PBPK
model parameters used as such quantifying the basic model
structure. The only information missing at this point is the CIP
dose administered intravenously. In accordance with the
experimental PK data, an i.v. dose of 200 mg CIP is consid-
ered here. Figure 5a shows the result of a 24-hour simulation
of the i.v. CIP PBPK model, as well as the corresponding
observed PK plasma data.100 In an actual pharmaceutical
development program, this single step can potentially involve
several iterations of parameter optimization, and bring about
the identification of structural changes in the model.101
In the next step, the oral administration of CIP was con-
sidered. The dataset from the study by Davis et al.100 is
particularly well suited for this purpose because it contains
a crossover study in which CIP was administered to the
same patients both i.v. and p.o. The missing model param-
eters for oral administration are relevant only to absorption
in the GI tract. First, the specific drug formulation needs to
be considered. A Weibull function was assumed to quantify
dissolution of the tablet (Table 1C). Together with formulation
release, the physicochemical solubility of CIP (Table 1A)
and the estimation of the intestinal permeability (Table 1C)
are sufficient to quantify absorption of a CIP tablet in the GI
tract. As previously discussed, the physiological processes
implemented
above
for
the
i.v.
remain
unchanged, such that CIP ADME can now be fully repre-
sented with the PBPK model. Figure 5b shows the result of
a 24-hour simulation of the p.o. CIP PBPK model, as well as
the corresponding PK plasma data for an oral CIP dose of
750 mg.100 The resulting PBPK model can now be used to
assess different administration schemes, to simulate virtual
populations, or to extrapolate the data to special popula-
tions.5 As a validation of model predictions, the model was
used to simulate the administration of 500 mg b.i.d. and
1,000 mg q.d., and the model predictions were compared
with the data available in the publication by Schuck et al.18
As can be seen from Figure 5c,d, the model is able to
describe both doses as well.
Having established a PBPK model for i.v. and p.o. admin-
istration of CIP, as next step such model was applied to fur-
ther PD analyses. As mentioned above, CIP is routinely
used in
clinical
practice
for
the
treatment
of
E. coli
Table 1A Physicochemical parameters
Value
Value
logP
0.95
pKa (acid)
6.1
MW
331 g/mol
pKa (base)
8.6
MW (effective)*
314 g/mol
fu in human
0.67
Solubility
6.18 mg/ml
These parameters represent the a priori input parameters for the drug.
*CIP contains a fluorine atom that leads to a reduction of the effective MW.
Table 1B Metabolization and excretion
Process
CYP1A2 metabolization
17 ml/min (intrinsic clearance)
Biliary secretion
1.03 ml/min/kg
Renal excretion
GFR specific: 0.266 ml/min/g of organ
TBS: 0.57 l/min
These parameters have been estimated from the plasma drug concentration.
GFR, glomerular filtration rate; TBS, tubular secretion
Table 1C Oral absorption.
Process
Parameter/Function
Drug dissolution in the GI tract (Weibull)
time (50%):4 min
lag time: 0 min
Shape: 0.8
Transcellular intestinal permeability
1E-06 cm/min
Small intestine transit time
4h
These
parameters
have
been
estimated
from
the
plasma
concentration.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

infections. An adaptive in vitro Emax model for CIP treat-
ment of infections with the microbial strain E. coli (11775)
was
previously
established.18
The
model
allows
the
description of microbial growth as well as CIP-mediated
inhibition such that time-kill profiles can be mechanistically
analyzed.
The
model
hence
quantifies
growth
in
the
absence as well as in the presence of CIP treatment, and
shows an initial phase of rapid killing followed by the devel-
opment of an adaptive resistance that slows the killing rate
in the presence of CIP.
dN
dt 5
k2
k1  ð12
Cr
IC501Cr


1k2
EC501C
 C

@

---CHUNK_BREAK---

dt 5 k2 k1  ð12 Cr IC501Cr   1k2 EC501C  C @ A  N  12ezt


(3)
Here, N is the bacterial count (CFU), k is the growth rate,
k1 is the initial kill rate constant, k2 is the permanent kill
rate constant, C is the lung interstitial concentration, i.e.,
the site of infection, and z accounts for the initial lag phase
(Table 1D). Cr is the drug concentration inducing adaptive
resistance (Table 1E):
Cr5C0 
e2ke t2tlag
ð
Þ2e2kecr t2tlag
ð
Þ


(4)
In this equation, C0 is the initial CIP concentration in the
experiment, ke is the simulated elimination rate constant, kecr
is the decline of the adaptive resistance (Table 1E), tlag is
the lag time until development of adaptive resistance sets in,
EC50 is the concentration of CIP that gives half-maximal
response, and IC50 is the concentration at 50% of maximum
resistance. The adaptive Emax model has been validated
using in vitro data on the growth of E. coli in the presence of
different in vitro CIP concentrations18 (Figure 5e).
Figure 5 (a) PBPK simulations for 200 mg CIP (i.v.).100 (b) PBPK simulation for 750 mg CIP (p.o.).100 (c) PBPK simulation for 500 mg b.i.d.
(p.o.).18 (d) PBPK simulation for 1,000 mg q.d. (p.o.).18 (e) PD simulations with an adaptive Emax model that describes time-kill profiles of E.
coli (11775) in the context of various in vitro doses of CIP.18 (f) PBPK/PD simulations. q.d., once-a-day dosing; b.i.d., twice-a-day dosing.

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License The CIP PBPK model and the PD model for CIP treatment
of respiratory tract infections of E.

coli infections can now be
combined to generate a full-blown PBPK/PD model.

In a previ-
ous PK/PD study, an initial CIP concentration was calculated
from a simulated 24-hour area AUC vs.

time curve (AUC24)/
MIC ratio (C0’5 2.43 mg/l).18 Using the lung interstitial con-
centration in the PBPK/PD as input in the adaptive Emax mod-
el, the therapeutic effect of 1,000 mg once-daily (q.d.) and
500 mg twice-daily (b.i.d.) of CIP was simulated for this bacte-
rial strain (Figure 5f).

As reported before, the time kill curve
for both dosing regimens show an equally effective decrease
in CFU/ml >5 log units over the first 24 hours.18 As also
reported in the literature, this is related to the use of an E.

coli
strain extremely sensitive to CIP, for which the 500 mg b.i.d.

dosing regimen was already high enough to promote maxi-
mum bacterial killing.

Notably, the presented PBPK/PD model
could now be the starting point for further investigations involv-
ing, for example, dedicated disease models of bacterial infec-
tions in specific tissues or usage of interstitial or intracellular
target tissue concentrations as effective input concentrations.

SUMMARY
In conclusion, PBPK models can be a valuable support in
drug development, in particular considering the possibility to
generate a priori simulations.

As a consequence, they are
increasingly used in pharmaceutical companies and regulato-
ry agencies like the US Food and Drug Administration.

Such
model development is possible, on the one hand, thanks to
the collection of physiological and anatomical information as
well as models that relate the physicochemical properties of a
molecule to its permeability and partition properties.

On the
other hand, during the model building process model assump-
tions should be carefully considered and components included
in the model should be in agreement with physiological and
pharmacological information available for the considered com-
pound.

Such assumptions should also be clearly kept in mind
when using the model for simulation and extrapolation.

Together with assumptions regarding the processes included
in the model, also assumptions relative to the physiological
and anatomical information incorporated from the database
should be carefully evaluated, in particular when considering
diseased populations for which in many instances such infor-
mation is not available or extremely variable.

Conflict of Interest.

L.K., C.N., T.W., J-F.S., M.B., T.E., and D.T.

are employees of Bayer Technology Services, S.W.

and J.L.

are employ-
ees of Bayer HealthCare.

1.

Peters, S.A.

Physiologically-Based Pharmacokinetic (PBPK) Modeling and Simula-
tions: Principles, Methods, and Applications in the Pharmaceutical Industry (John
Wiley & Sons, Hoboken, NJ, 2012).

2.

Proctor, N.J., Tucker, G.T.

& Rostami-Hodjegan, A.

Predicting drug clearance from
recombinantly expressed CYPs: intersystem extrapolation factors.

Xenobiotica 34,
151–178 (2004).

3.

Meyer, M., Schneckener, S., Ludewig, B., Kuepfer, L.

& Lippert, J.

Using expression
data for quantification of active processes in physiologically based pharmacokinetic
modeling.

Drug Metab.

Dispos.

40, 892–901 (2012).

4.

Jones, H.

& Rowland-Yeo, K.

Basic concepts in physiologically based pharmacoki-
netic modeling in drug discovery and development.

CPT Pharmacometrics Syst.

Pharmacol.

2, e63 (2013).

5.

Maharaj, A.R.

& Edginton, A.N.

Physiologically based pharmacokinetic modeling and
simulation in pediatric drug development.

CPT Pharmacometrics Syst.

Pharmacol.

3,
e150 (2014).

6.

Jadhav, P.R.

et al.

A proposal for scientific framework enabling specific population
drug dosing recommendations.

J.

Clin.

Pharmacol.

55, 1073–1078 (2015).

7.

Jiang, X.L., Zhao, P., Barrett, J.S., Lesko, L.J.

& Schmidt, S.

Application of physio-
logically based pharmacokinetic modeling to predict acetaminophen metabolism and
pharmacokinetics in children.

CPT Pharmacometrics Syst.

Pharmacol.

2, (e80)
(2013).

8.

Edginton, A.N.

& Willmann, S.

Physiology-based simulations of a pathological condi-
tion: prediction of pharmacokinetics in patients with liver cirrhosis.

Clin.

Pharmacoki-
net.

47, 743–752 (2008).

9.

Sinha, V.K.

et al.

From preclinical to human -prediction of oral absorption and drug-
drug interaction potential using physiologically based pharmacokinetic (PBPK)
modeling approach in an industrial setting: a workflow by using case example.

Bio-
pharm.

Drug Dispos.

33, 111–121 (2012).

10.

Schaller, S.

et al.

A generic integrated physiologically based whole-body model of
the glucose-insulin-glucagon regulatory system.

CPT Pharmacometrics Syst.

Phar-
macol.

2, e65 (2013).

11.

Willmann, S., Thelen, K., Becker, C., Dressman, J.B.

& Lippert, J.

Mechanism-based
prediction of particle size-dependent dissolution and absorption: cilostazol pharmaco-
kinetics in dogs.

Eur.

J.

Pharm.

Biopharm.

76, 83–94 (2010).

12.

Thiel, C.

et al.

A systematic evaluation of the use of physiologically based pharma-
cokinetic modeling for cross-species extrapolation.

J.

Pharm.

Sci.

104, 191–206
(2015).

13.

Jones HM, Parrott N, Jorga K, Lave T.

A novel strategy for physiologically based
predictions of human pharmacokinetics.

Clin.

Pharmacokinet.

45, 511–542 (2006).

14.

Eissing, T.

et al.

A computational systems biology software platform for multiscale
modeling and simulation: integrating whole-body physiology, disease biology, and
molecular reaction networks.

Front.

Physiol.

2, 4 (2011).

15.

Krauss, M.

et al.

Integrating cellular metabolism into a multiscale whole-body model.

PLoS Comput.

Biol.

8, e1002750 (2012).

16.

Schwen, L.O.

et al.

Spatio-temporal simulation of first pass drug perfusion in the liv-
er.

PLoS Comput.

Biol.

10, e1003499 (2014).

17.

Krauss, M.

et al.

Using Bayesian-PBPK modeling for assessment of inter-individual
variability and subgroup stratification.

In Silico Pharmacol.

1, 6 (2013).

18.

Schuck, E.L., Dalhoff, A., Stass, H.

& Derendorf, H.

Pharmacokinetic/pharmacodynamic
(PK/PD) evaluation of a once-daily treatment using ciprofloxacin in an extended-release
dosage form.

Infection.

33(suppl.

2), 22–28 (2005).

19.

Simeoni, M.

et al.

Predictive pharmacokinetic-pharmacodynamic modeling of tumor
growth kinetics in xenograft models after administration of anticancer agents.

Cancer
Res.

64, 1094–1101 (2004).

20.

Riggs, M.M., Bennetts, M., van, der Graaf P.H.

& Martin, S,W.

Integrated pharmaco-
metrics and systems pharmacology model-based analyses to guide GnRH receptor
modulator development for management of endometriosis.

CPT Pharmacometrics
Syst.

Pharmacol.

1, e11 (2012).

21.

Thiel, C.

et al.

Model-based contextualization of in vitro toxicity data quantitatively
predicts in vivo drug response in patients.

Arch.

Toxicol.

(2016) [Epub ahead of
print].

22.

Burghaus, R.

et al.

Computational investigation of potential dosing schedules for a
switch of medication from warfarin to rivaroxaban-an oral, direct Factor Xa inhibitor.

Front.

Physiol.

5, 417 (2014).

23.

Danhof M.

Systems pharmacology — Towards the modeling of network interactions.

Eur.

J.

Pharm.

Sci.; e-pub ahead of print 2016.

24.

Liu, X.

et al.

Use of a physiologically based pharmacokinetic model to study the
time to reach brain equilibrium: an experimental analysis of the role of blood-brain
barrier permeability, plasma protein binding, and brain tissue binding.

J.

Pharmacol.

Exp.

Ther.

313, 1254–1262 (2005).

25.

Hoehme, S.

et al.

Prediction and validation of cell alignment along microvessels as
order principle to restore tissue architecture in liver regeneration.

Proc.

Natl.

Acad.

Sci.

U.

S.

A.

107, 10371–10376 (2010).

26.

Niederalt, C.

et al.

Development of a physiologically based computational kidney
model to describe the renal excretion of hydrophilic agents in rats.

Front.

Physiol.

3,
494 (2012).

Table 1D Bacterial growth model
k (h21)
k1 (h21)
k2 (h21)
EC50 (mg/l)
IC50 (mg/l)
z (h21)
7.76
10.8
8.4
0.0035
0.00047
0.09
These parameters are provided in the literature (95).

Table 1E Adaptive resistance
tlag (h)
kecr (h21)
ke (h21)

0.014
These parameters are provided in the literature (95).

---CHUNK_BREAK---

tlag (h) kecr (h21) ke (h21) 0.014 These parameters are provided in the literature (95).  21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

---CHUNK_BREAK---

Library for rules of use; OA articles are governed by the applicable Creative Commons License 27. Thomas, S.R. Kidney modeling and systems physiology. Wiley Interdiscipl. Rev. Syst. Biol. Med. 1, 172–190 (2009). 28. Tawhai, M.H. & Bates, J.H. Multi-scale lung modeling. J. Appl. Physiol. 110,
1466–1472 (2011). 29. Thelen, K. et al. Evolution of a detailed physiological model to simulate the gastroin-
testinal transit and absorption process in humans, part 1: oral solutions. J. Pharm. Sci. 100, 5324–5345 (2011). 30. Thelen, K., Coboeken, K., Willmann, S., Dressman, J.B. & Lippert, J. Evolution of a
detailed physiological model to simulate the gastrointestinal transit and absorption
process in humans, part II: extension to describe performance of solid dosage
forms. J. Pharm. Sci. 101, 1267–1280 (2012). 31. Agoram, B., Woltosz, W.S. & Bolger, M.B. Predicting the impact of physiological
and biochemical processes on oral drug bioavailability. Adv. Drug Del. Rev. 50(Suppl 1), S41–67 (2001). 32. Levitt, D.G. Physiologically based pharmacokinetic modeling of arterial — antecubital
vein concentration difference. BMC Clin. Pharmacol. 4, 2 (2004). 33. Musther, H. et al. Are physiologically based pharmacokinetic models reporting the
right Cmax? Central venous versus peripheral sampling site. AAPS J. 17,
1268–1279 (2015). 34. Thelen, K. & Dressman, J.B. Cytochrome P450-mediated metabolism in the human
gut wall. J. Pharm. Pharmacol. 61, 541–558 (2009). 35. Lennernas, H. Intestinal permeability and its relevance for absorption and elimina-
tion. Xenobiotica 37, 1015–1051 (2007). 36. Willmann, S., Schmitt, W., Keldenich, J., Lippert, J. & Dressman, J.B. A physiologi-
cal model for the estimation of the fraction dose absorbed in humans. J. Med. Chem. 47, 4022–4031 (2004). 37. Kilford, P.J., Gertz, M., Houston, J.B. & Galetin, A. Hepatocellular binding of drugs:
correction for unbound fraction in hepatocyte incubations using microsomal binding
or drug lipophilicity data. Drug Metab. Dispos. 36, 1194–1197 (2008). 38. Dressman, J.B., Amidon, G.L., Reppas, C. & Shah, V.P. Dissolution testing as a
prognostic tool for oral drug absorption: immediate release dosage forms. Pharm. Res. 15, 11–22 (1998). 39. Cardot, J., Beyssac, E. & Alric, M. In vitro-in vivo correlation: importance of dissolu-
tion in IVIVC. Dissolut. Technol. 14, 15 (2007). 40. Costa, P. & Sousa Lobo, J.M. Modeling and comparison of dissolution profiles. Eur. J. Pharm. Sci. 13, 123–133 (2001). 41. Blakey, G.E., Nestorov, I.A., Arundel, P.A., Aarons, L.J. & Rowland, M. Quantitative
structure-pharmacokinetics relationships: I. Development of a whole-body physiologi-
cally based model to characterize changes in pharmacokinetics across a homolo-
gous series of barbiturates in the rat. J. Pharmacokinet. Biopharm. 25, 277–312
(1997). 42. Jones, H.M., Gardner, I.B. & Watson, K.J. Modelling and PBPK simulation in drug
discovery. AAPS J. 11, 155–166 (2009). 43. Poulin, P., Schoenlein, K. & Theil, F.P. Prediction of adipose tissue: plasma partition
coefficients for structurally unrelated drugs. J. Pharm. Sci. 90, 436–447 (2001). 44. Poulin, P. & Theil, F.P. A priori prediction of tissue:plasma partition coefficients of
drugs to facilitate the use of physiologically-based pharmacokinetic models in drug
discovery. J. Pharm. Sci. 89, 16–35 (2000). 45. Rodgers, T., Leahy, D. & Rowland, M. Physiologically based pharmacokinetic
modeling 1: predicting the tissue distribution of moderate-to-strong bases. J. Pharm. Sci. 94, 1259–1276 (2005). 46. Rodgers, T. & Rowland, M. Physiologically based pharmacokinetic modelling 2: pre-
dicting the tissue distribution of acids, very weak bases, neutrals and zwitterions. J. Pharm. Sci. 95, 1238–1257 (2006). 47. Berezhkovskiy, L.M. Volume of distribution at steady state for a linear pharmacoki-
netic system with peripheral elimination. J. Pharm. Sci. 93, 1628–1640 (2004). 48. Willmann, S., Lippert, J. & Schmitt, W. From physicochemistry to absorption and dis-
tribution: predictive mechanistic modelling and computational tools. Expert Opin. Drug Metabol. Toxicol. 1, 159–168 (2005). 49. Willmann, S. et al. PK-SimV
R : a physiologically based pharmacokinetic ‘‘whole-body’’
model. Biosilico. 1, 121–124 (2003). 50. Loidl-Stahlhofen, A. et al. Multilamellar liposomes and solid-supported lipid mem-
branes (TRANSIL): screening of lipid-water partitioning toward a high-throughput
scale. Pharm. Res. 18, 1782–1788 (2001). 51. Leahy, D., Lynch, J. & Taylor, D. Mechanisms of Absorption of Small Molecules. Novel Drug Delivery and Its Therapeutic Application (Wiley, New York, 1989). 52. Schmitt, W. General approach for the calculation of tissue to plasma partition coeffi-
cients. Toxicol. In Vitro 22, 457–467 (2008). 53. Levitt, D.G. PKQuest: capillary permeability limitation and plasma protein binding —
application to human inulin, dicloxacillin and ceftriaxone pharmacokinetics. BMC
Clin. Pharmacol. 2, 7 (2002). 54. Levin, V.A., Dolginow, D., Landahl, H.D., Yorke, C. & Csejtey, J. Relationship of
octanol/water partition coefficient and molecular weight to cellular permeability and
partitioning in s49 lymphoma cells. Pharm. Res. 1, 259–266 (1984). 55. Lieb, W.R. & Stein, W.D. Biological membranes behave as non-porous polymeric
sheets with respect to the diffusion of non-electrolytes. Nature. 224, 240–243
(1969). 56. Kawai, R. et al. Physiologically based pharmacokinetic study on a cyclosporin deriv-
ative, SDZ IMM 125. J. Pharmacokinet. Biopharm. 22, 327–365 (1994). 57. Sugano, K., Nabuchi, Y., Machida, M. & Aso, Y. Prediction of human intestinal
permeability using artificial membrane permeability. Int. J. Pharm. 257, 245–251
(2003). 58. Artursson, P. & Karlsson, J. Correlation between oral drug absorption in humans
and apparent drug permeability coefficients in human intestinal epithelial (Caco-2)
cells. Biochem. Biophys. Res. Commun. 175, 880–885 (1991). 59. Irvine, J.D. et al. MDCK (Madin-Darby canine kidney) cells: A tool for membrane
permeability screening. J. Pharm. Sci. 88, 28–33 (1999). 60. Grass, G.M. & Sweetana, S.A. In vitro measurement of gastrointestinal tissue per-
meability using a new diffusion cell. Pharm. Res. 5, 372–376 (1988). 61. Salphati, L., Childers, K., Pan, L., Tsutsui, K. & Takahashi, L. Evaluation of a
single-pass intestinal-perfusion method in rat for the prediction of absorption in man. J. Pharm. Pharmacol. 53, 1007–1013 (2001). 62. Kumar, S. et al. Extrapolation of diclofenac clearance from in vitro microsomal
metabolism data: role of acyl glucuronidation and sequential oxidative metabolism of
the acyl glucuronide. J. Pharmacol. Exp. Ther. 303, 969–978 (2002). 63. Kusuhara, H. & Sugiyama, Y. In vitro-in vivo extrapolation of transporter-mediated
clearance in the liver and kidney. Drug Metab. Pharmacokinet. 24, 37–52 (2009). 64. Lippert, J. et al. A mechanistic, model-based approach to safety assessment in clini-
cal development. CPT Pharmacometrics Syst. Pharmacol. 1, e13 (2012). 65. Wilkinson, G.R. Clearance approaches in pharmacology. Pharmacol. Rev. 39, 1–47
(1987). 66. Rostami-Hodjegan, A. & Tucker, G.T. Simulation and prediction of in vivo drug metabo-
lism in human populations from in vitro data. Nat. Rev. Drug Disc. 6, 140–148 (2007). 67. Jamei, M., Dickinson, G.L. & Rostami-Hodjegan, A. A framework for assessing inter-
individual variability in pharmacokinetics using virtual human populations and inte-
grating general knowledge of physical chemistry, biology, anatomy, physiology and
genetics: A tale of ’bottom-up’ vs ’top-down’ recognition of covariates. Drug Metab. Pharmacokinet. 24, 53–75 (2009). 68. Harwood, M.D. et al. Absolute abundance and function of intestinal drug transport-
ers: a prerequisite for fully mechanistic in vitro-in vivo extrapolation of oral drug
absorption. Biopharm. Drug Dispos. 34, 2–28 (2013). 69. Block, M. Physiologically based pharmacokinetic and pharmacodynamic modeling in
cancer drug development: status, potential and gaps. Expert Opin. Drug Metab. Tox-
icol. 11. 743–756 (2015). 70. Wang, W., Wang, E.Q. & Balthasar, J.P. Monoclonal antibody pharmacokinetics and
pharmacodynamics. Clin. Pharmacol. Ther. 84, 548–558 (2008). 71. Agoram, B.M., Martin, S.W. & van der Graaf, P.H. The role of mechanism-based
pharmacokinetic-pharmacodynamic (PK-PD) modelling in translational research of
biologics. Drug Discov. Today. 12, 1018–1024 (2007). 72. Baumann, A.

---CHUNK_BREAK---

modelling in translational research of biologics. Drug Discov. Today. 12, 1018–1024 (2007). 72. Baumann, A. Early development of therapeutic biologics—pharmacokinetics.

Curr.

Drug Metab.

7, 15–21 (2006).

73.

Lobo, E.D., Hansen, R.J.

& Balthasar, J.P.

Antibody pharmacokinetics and pharma-
codynamics.

J.

Pharm.

Sci.

93, 2645–2668 (2004).

74.

Baxter, L., Zhu, H., Mackensen, D., Butler, W.

& Jain, R.

Biodistribution of monoclo-
nal antibodies: scale-up from mouse to human using a physiologically based phar-
macokinetic model.

Cancer Res.

55, 4611–4622 (1995).

75.

Baxter, L., Zhu, H., Mackensen, D.

& Jain, R.

Physiologically based pharmacokinetic
model for specific and nonspecific monoclonal antibodies and fragments in normal tis-
sues and human tumor xenografts in nude mice.

Cancer Res.

54, 1517–1528 (1994).

76.

Chabot,
J.R.,
Dettling,
D.E.,
Jasper,
P.J.

&
Gomes,
BC.

Comprehensive
mechanism-based antibody pharmacokinetic modeling.

Conference Proceedings:
Annual International Conference of the IEEE Engineering in Medicine and Biology
Society IEEE Engineering in Medicine and Biology Society Annual Conference,
4318–4323 (2011).

77.

Chen, Y.

& Balthasar, J.P.

Evaluation of a catenary PBPK model for predicting the
in vivo disposition of mAbs engineered for high-affinity binding to FcRn.

AAPS J.

14, 850–859 (2012).

78.

Davda, J., Jain, M., Batra, S., Gwilt, P.

& Robinson, D.

A physiologically based
pharmacokinetic (PBPK) model to characterize and predict the disposition of mono-
clonal antibody CC49 and its single chain Fv constructs.

Int.

Immunopharmacol.

8,
401–413 (2008).

79.

Ferl, G., Kenanova, V., Wu, A.

& DiStefano, J.

III.

A two-tiered physiologically based
model for dually labeled single-chain Fv-Fc antibody fragments.

Mol.

Cancer Ther.

5, 1550 (2006).

80.

Ferl, G., Wu, A.

& DiStefano, J.

A predictive model of therapeutic monoclonal anti-
body dynamics and regulation by the neonatal Fc receptor (FcRn).

Ann.

Biomed.

Eng.

33, 1640–1652 (2005).

81.

Fronton, L., Pilari, S.

& Huisinga, W.

Monoclonal antibody disposition: a simplified
PBPK model and its implications for the derivation and interpretation of classical
compartment models.

J.

Pharmacokinet.

Pharmacodyn.

41, 87–107 (2014).

82.

Garg, A.

& Balthasar, J.

Physiologically-based pharmacokinetic (PBPK) model to
predict IgG tissue kinetics in wild-type and FcRn-knockout mice.

J.

Pharmacokinet.

Pharmacodyn.

34, 687–709 (2007).

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

83.
Sepp, A., Berges, A., Sanderson, A. & Meno-Tetang, G. Development of a physio-
logically based pharmacokinetic model for a domain antibody in mice using the two-
pore theory. J. Pharmacokinet. Pharmacodyn. 42, 97–109 (2015).
84.
Shah, D.K. & Betts, A.M. Towards a platform PBPK model to characterize the plas-
ma and tissue disposition of monoclonal antibodies in preclinical species and
human. J. Pharmacokinet. Pharmacodyn. 39, 67–86 (2012).
85.
Rippe, B. & Haraldsson, B. Fluid and protein fluxes across small and large pores in
the microvasculature. Application of two-pore equations. Acta Physiol. Scand. 131,
411–428 (1987).
86.
Rippe, B. & Haraldsson, B. Transport of macromolecules across microvascular walls:
the two-pore theory. Physiol. Rev. 74, 163–219 (1994).
87.
Chen, X., Hickling, T.P. & Vicini, P. A mechanistic, multiscale mathematical model
of immunogenicity for therapeutic proteins: part 1-theoretical model. CPT Pharmaco-
metrics Syst. Pharmacol. 3, e133 (2014).
88.
Chen, X., Hickling, T.P. & Vicini, P. A mechanistic, multiscale mathematical model
of immunogenicity for therapeutic proteins. Part 2. model applications. CPT Pharma-
cometrics Syst. Pharmacol. 3, e134 (2014).
89.
European Medicines Agency Committee for Medicinal Products for Human Use:
Concept Paper on Qualification and reporting of physiologically-based pharmacoki-
netic (PBPK) modeling and analyses. EMA/CHMP/211243/2014 (2014).
90.
Jones, H.M. et al. Physiologically based pharmacokinetic modeling in drug discovery
and development: a pharmaceutical industry perspective. Clin. Pharmacol. Ther. 97,
247–262 (2015).
91.
Sager, J.E., Yu, J., Raguenau-Majlessi, I. & Isoherranen, N. Physiologically based
pharmacokinetic (PBPK) modeling and simulation approaches: a systematic review
of published models, applications and model verification. Drug Metab. Dispos.; e-
pub ahead of print 2015.
92.
Shepard, T., Scott, G., Cole, S., Nordmark, A., & Bouzom, F. Physiologically based mod-
els in regulatory submissions: output from the ABPI/MHRA forum on physiologically based
modeling and simulation. CPT Pharmacometrics Syst. Pharmacol. 4, 221–225 (2015).
93.
Wagner, C. et al. Application of physiologically based pharmacokinetic (PBPK)
modeling to support dose selection: report of an FDA Public Workshop on PBPK.
CPT Pharmacometrics Syst. Pharmacol. 4, 226–230 (2015).
94.
Zhao, P., Rowland, M. & Huang, SM. Best practice in the use of physiologically
based pharmacokinetic modeling and simulation to address clinical pharmacology
regulatory questions. Clin. Pharmacol. Ther. 92, 17–20 (2012).
95.
Leong, R. et al. Regulatory experience with physiologically based pharmacoki-
netic modeling for pediatric drug trials. Clin. Pharmacol. Ther. 91, 926–931
(2012).
96.
McLellan, R.A., Drobitch, R.K., Monshouwer, M. & Renton, KW. Fluoroquinolone
antibiotics inhibit cytochrome P450-mediated microsomal drug metabolism in rat and
human. Drug Metab. Dispos. 24, 1134–1138 (1996).
97.
Ball, C.S., Manson, J.M., Reid, F. & Tweedle, D.E. The pharmacokinetics of
the biliary excretion of ciprofloxacin. HPB Surg. 1, 319–326 discussion 26-27
(1989).
98.
Drusano, G.L. An overview of the pharmacology of intravenously administered cipro-
floxacin. Am. J. Med. 82, 339–345 (1987).
99.
Bergan, T., Thorsteinsson, S.B., Kolstad, I.M. & Johnsen, S. Pharmacokinetics of ciprofloxa-
cin after intravenous and increasing oral doses. Eur. J. Clin. Microbiol. 5, 187–192 (1986).
100.
Davis, R.L. et al. Pharmacokinetics of ciprofloxacin in cystic fibrosis. Antimicrob.
Agents Chemother. 31, 915–919 (1987).
101.
Kuepfer, L., Peter, M., Sauer, U. & Stelling, J. Ensemble modeling for analysis of
cell signaling dynamics. Nat. Biotechnol. 25, 1001–1006 (2007).
V
C
2016 The Authors CPT: Pharmacometrics & Systems
Pharmacology published by Wiley Periodicals, Inc. on
behalf of American Society for Clinical Pharmacology and
Therapeutics. This is an open access article under the
terms of the Creative Commons Attribution-NonCommer-
cial-NoDerivs License, which permits use and distribution
in any medium, provided the original work is properly cit-
ed, the use is non-commercial and no modifications or
adaptations are made.
Supplementary information accompanies this paper on the CPT: Pharmacometrics & Systems Pharmacology website
(http://www.wileyonlinelibrary.com/psp4)

 21638306, 2016, 10, Downloaded from https://ascpt.onlinelibrary.wiley.com/doi/10.1002/psp4.12134 by Spanish Cochrane National Provision (Ministerio de Sanidad), Wiley Online Library on [28/07/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License