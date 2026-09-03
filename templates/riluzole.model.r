#------------------------------------------------------------------------------
#volume is in Kg
#Blood flow is in L/hr
#concentration is ug/L.
#Amount is ug
#dose is ug/Kg BW/day.
#Aurine is in ug
#Afeces is in ug.
#M1 represent metabolite

States  = {
Astomach,
Agut,
Aliver,						
Abrain,
Akidney,
Alung,
Afat,
Amuscle,
Aheart,
Arestbody,
Aplasma,
Aurine,
Afeces,
AliverM1,
AbrainM1,
AkidneyM1,
AlungM1,
AfatM1,
AmuscleM1,
AheartM1,
ArestbodyM1,
AplasmaM1,
AurineM1}; 

Outputs = {cliver, cbrain, ckidney, clung, cfat, cmuscle, cheart, crestbody, cplasma, 
          cliverM1, cbrainM1, ckidneyM1, clungM1, cfatM1, cmuscleM1, cheartM1, crestbodyM1, cplasmaM1,
		  vgut,vliver,vbrain,vkidney,vlung,vfat,vmuscle,vheart,vrestbody,vplasma,mass_vol,
		  Qgut,Qliver,Qbrain,Qkidney,Qlung,Qfat,Qmuscle,Qheart,Qrestbody,QCplasma,mass_blood};

Inputs={oraldose}; 

#dosing schedule 
dosing = 1;                                       
intT = 0;
expT = 1.E-3;
period = 1;
dose=1;


#######################################################################
#Rat Physiological parameters
###################################################################################

BW = 0.25;						#Rat data

#constant Fraction of blood flows to organs (blood flow rate)
QCC = 18.7;                   #Total Cardiac blood output (L/h/kg)  #Riluzole model
HCT = 0.46; 				 #hematocrit percentage  #flutamide model

FQgut = 0.075;  			 #Fraction cardiac output going to gut  https://sci-hub.se/10.1023/a:1018943613122  davies et al. 1993

FQliver = 0.174;		     #Fraction cardiac output going to liver   #Riluzole model
FQbrain = 0.02;				 #Fraction cardiac output going to brain
FQkidney = 0.141;            #Fraction cardiac output going to kidney
FQlung = 0.021;				 #Fraction cardiac output going to Lung
FQfat =  0.07; 		         #Fraction cardiac output going to fat  
FQmuscle = 0.278; 		     #Fraction cardiac output going to muscle
FQheart = 0.051; 		     #Fraction cardiac output going to muscle  





#constant organ volume as a fraction of total body weight
Fgut = 0.027;  				 #fractional volume of gut     (0.46+1.40+0.84) brown et al. 1997
Fliver = 0.036;		         #Fraction liver volume 
Fbrain = 0.006;			     #Fraction brain volume
Fkidney = 0.0073;            #Fraction kidney volume	
Flung = 0.006;			     #Fraction brain volume
Ffat = 0.07;                 #fractional volume of fat 
Fmuscle= 0.488;	         		     #fractional volume of muscle, 122 ml =0.122 kg = 0.122*BW =0.122/0.25, this is for 280 g rat https://link-springer-com.sabidi.urv.cat/article/10.1007/s10928-011-9232-2/tables/2
              
Fheart=0.004;							#fractional volume of heart, 1.02 = 0.00102*BW=0.00102/0.25 , this is for 280 g rat https://link-springer-com.sabidi.urv.cat/article/10.1007/s10928-011-9232-2/tables/2

Fplasma = 0.074; 	         #fractional volume of plasma, to confirm once.




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Physicochemical parameter For chemical (change with chemical)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

MW = 234.2;										    # g/mol-1, riluzole

k_liver_plasma = 2.0;									#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/

k_brain_plasma = 2.44; 			                    #brain/blood partition coefficient, View of Brain and Plasma Riluzole Pharmacokinetics: Effect of Minocycline Combination (ualberta.ca)

k_kidney_plasma=0.1;

k_lung_plasma=0.1;

k_fat_plasma=0.1;

k_muscle_plasma=0.3;								#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/

k_heart_plasma=0.1;

k_restbody_plasma = 0.07;			                #Rest of the body/blood partition coefficient


k_liver_plasmaM1 = 2.0;

k_brain_plasmaM1 = 2.44; 			                    #brain/blood partition coefficient, View of Brain and Plasma Riluzole Pharmacokinetics: Effect of Minocycline Combination (ualberta.ca)

k_kidney_plasmaM1=0.1;

k_lung_plasmaM1=0.1;

k_fat_plasmaM1=0.1;

k_muscle_plasmaM1=0.1;								#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/

k_heart_plasmaM1=0.1;

k_restbody_plasmaM1 = 0.07;			                #Rest of the body/blood partition coefficient


GE=1.7;													#Optimized, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/
kgut=0.6;											#experimental data, 
kabs=9.99;												#absorption rate, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/
fu = 0.04;                                         #Free fraction of riluzole in plasma, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/
fu_M1 =0.001;

vmaxlivM1_invitro=0.0001;												#2500000 nmol/h/kg^0.75
kmliverM1=1;															#	50000 nmol/l


Cl = 0.0001;															#ml/h/kg^0.75,  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/
ClM1=0.0001;

Cl_feces=0.556;										#Set the first-order constant for gut absorption and fecal elimination from gut 9:1 (assuming approximately 90% absorption in humans) https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7253195/


#Data on metabolism

# microsomal proteins content, mg / gr 
MSPL = 60; 				# liver microsomal protein content (Brian Houston and Carlile, 1997) 

Tscale = 60;            # for conversion of min to hr in scaling function
vscale = 1000;			#for conversion of liver weight in g from kg for scaling MSP to whole liver


######################  ASD
#GE=1.7 (ASD)
#kgut=0.6
#fu=0.04
#kurineC=0.16

#############  Tablet
#GE=5.7
#Kgut=0.4;
#fu=0.19
#kurineC=0.16

###########################API
#GE=6.7
#Kgut=0.2;
#fu=0.2;
#kurineC=0.16

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Initialize
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Initialize{

}

Dynamics {  

QCblood = QCC*pow(BW,0.75); 															#L/hr
QCplasma =QCblood *(1-HCT); 
Qgut = FQgut*QCplasma; 					                                                                     #Adjust initial cardiac output for plasma flow
Qliver= FQliver* QCplasma;   	 				                    												 #Plasma flow to liver
Qbrain = FQbrain* QCplasma; 
Qkidney=FQkidney*QCplasma;
Qlung=FQlung*QCplasma;
Qfat=FQfat*QCplasma;
Qmuscle=FQmuscle*QCplasma;
Qheart=FQheart*QCplasma;
Qrestbody = QCplasma-(Qgut+ Qliver + Qbrain + Qkidney + Qlung + Qfat + Qmuscle + Qheart);

mass_blood=(Qgut+Qliver+Qbrain + Qkidney + Qlung + Qfat + Qmuscle + Qheart+Qrestbody)-QCplasma;

vgut = Fgut*BW;
vliver =  Fliver * BW ;
vbrain = Fbrain * BW;
vkidney=Fkidney*BW;
vlung=Flung*BW;
vfat=Ffat*BW;
vmuscle=Fmuscle*BW;
vheart=Fheart*BW;
vplasma = Fplasma*BW ;
vrestbody = (0.84*BW) - (vgut+vliver+vbrain+vkidney+vlung+vfat+vmuscle+vheart+vplasma);

mass_vol=(vgut+vliver+vbrain+vkidney+vlung+vfat+vmuscle+vheart+vplasma+vrestbody)-BW;

vmaxliverM1 = vmaxlivM1_invitro* MSPL* vliver* Tscale* vscale;       #microgram/hr/whole body
RAM1=vmaxliverM1*cliver*fu/(cliver*fu+kmliverM1);
kurine = Cl*pow(BW,0.75); 	  
kurineM1 = ClM1*pow(BW,0.75); 
kfeces=Cl_feces*pow(BW,0.75); 


cgut=Agut/vgut;
cliver=Aliver/vliver;
cbrain=Abrain/vbrain;
ckidney=Akidney/vkidney;
clung=Alung/vlung;
cfat=Afat/vfat;
cmuscle=Amuscle/vmuscle;
cheart=Aheart/vheart;
crestbody=Arestbody/vrestbody;
cplasma=Aplasma/vplasma;

################################Metabolite M1
cliverM1=AliverM1/vliver;
cbrainM1=AbrainM1/vbrain;
ckidneyM1=AkidneyM1/vkidney;
clungM1=AlungM1/vlung;
cfatM1=AfatM1/vfat;
cmuscleM1=AmuscleM1/vmuscle;
cheartM1=AheartM1/vheart;
crestbodyM1=ArestbodyM1/vrestbody;
cplasmaM1=AplasmaM1/vplasma;

dt(Astomach) = -GE*Astomach +(oraldose*BW)/expT;    
dt(Agut) = -kgut*Agut+ GE*Astomach - (kfeces* cgut);   

dt(Aliver) = kgut*Agut+Qliver*(cplasma*fu - cliver*(fu/k_liver_plasma))-RAM1;
dt(Abrain) = Qbrain *(cplasma*fu - cbrain*(fu/k_brain_plasma));  
dt(Akidney) = Qkidney *(cplasma*fu - ckidney*(fu/k_kidney_plasma));  
dt(Alung) = Qlung *(cplasma*fu - clung*(fu/k_lung_plasma));  
dt(Afat) = Qfat *(cplasma*fu - cfat*(fu/k_fat_plasma));  
dt(Amuscle) = Qmuscle *(cplasma*fu - cmuscle*(fu/k_muscle_plasma));  
dt(Aheart) = Qheart *(cplasma*fu - cheart*(fu/k_heart_plasma));  
dt(Arestbody)=Qrestbody *(cplasma*fu - crestbody*(fu/k_restbody_plasma));  

dt(Aplasma) = (Qliver*cliver*(fu/ k_liver_plasma)) +  (Qbrain*cbrain*(fu/k_brain_plasma)) + (Qkidney*ckidney*(fu/k_kidney_plasma)) +
(Qlung*clung*(fu/k_lung_plasma)) + (Qfat*cfat*(fu/k_fat_plasma)) + (Qmuscle*cmuscle*(fu/k_muscle_plasma)) +  (Qheart*cheart*(fu/k_heart_plasma)) +
(Qrestbody *crestbody*(fu/k_restbody_plasma)) - (QCplasma* cplasma*fu) - (kurine* cplasma);

dt(Aurine)= kurine* cplasma;  
dt(Afeces)= kfeces* cgut; 

dt(AliverM1) = RAM1+Qliver*(cplasmaM1*fu_M1 - cliverM1*(fu/k_liver_plasma));
dt(AbrainM1) = Qbrain *(cplasmaM1*fu_M1 - cbrainM1*(fu/k_brain_plasma));  
dt(AkidneyM1) = Qkidney *(cplasmaM1*fu_M1 - ckidneyM1*(fu/k_kidney_plasma));  
dt(AlungM1) = Qlung *(cplasmaM1*fu_M1 - clungM1*(fu/k_lung_plasma));  
dt(AfatM1) = Qfat *(cplasmaM1*fu_M1 - cfatM1*(fu/k_fat_plasma));  
dt(AmuscleM1) = Qmuscle *(cplasmaM1*fu_M1 - cmuscleM1*(fu/k_muscle_plasma));  
dt(AheartM1) = Qheart *(cplasmaM1*fu_M1 - cheartM1*(fu/k_heart_plasma));  
dt(ArestbodyM1)=Qrestbody *(cplasmaM1*fu_M1 - crestbodyM1*(fu/k_restbody_plasma));  

dt(AplasmaM1) = (Qliver*cliverM1*(fu_M1/k_liver_plasma)) +  (Qbrain*cbrainM1*(fu_M1/k_brain_plasma)) + (Qkidney*ckidneyM1*(fu_M1/k_kidney_plasma)) +
(Qlung*clungM1*(fu_M1/k_lung_plasma)) + (Qfat*cfatM1*(fu_M1/k_fat_plasma)) + (Qmuscle*cmuscleM1*(fu_M1/k_muscle_plasma)) +  (Qheart*cheartM1*(fu_M1/k_heart_plasma)) +
(Qrestbody *crestbodyM1*(fu_M1/k_restbody_plasma)) - (QCplasma* cplasmaM1*fu_M1) - (kurineM1* cplasmaM1);

dt(AurineM1)= kurineM1* cplasmaM1;  
  
} 
  


End.