from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document


#Extract Data From the PDF File
def load_pdf_file(data):
    loader= DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)

    documents=loader.load()

    return documents



def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs



#Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks



#Download the Embeddings from HuggingFace 
def download_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings


def get_medical_knowledge_documents() -> List[Document]:
    """Generate comprehensive medical knowledge as Document objects."""
    knowledge = [
        # DIABETES
        ("Diabetes Mellitus is a chronic metabolic disorder characterized by elevated blood glucose levels. "
         "Type 1 diabetes is an autoimmune condition where the pancreas produces little or no insulin. "
         "Type 2 diabetes occurs when the body becomes resistant to insulin or doesn't produce enough. "
         "Symptoms include frequent urination, excessive thirst, unexplained weight loss, fatigue, and blurred vision. "
         "Treatment for Type 1 requires insulin therapy. Type 2 may be managed with metformin, lifestyle changes, "
         "diet modification, and exercise. HbA1c test measures average blood sugar over 2-3 months. "
         "Target HbA1c is below 7% for most adults. Complications include neuropathy, retinopathy, nephropathy, "
         "and cardiovascular disease. Regular monitoring of blood glucose is essential.",
         "diabetes"),

        # HYPERTENSION
        ("Hypertension (High Blood Pressure) is defined as blood pressure consistently at or above 130/80 mmHg. "
         "It is called the 'silent killer' because it often has no symptoms. Risk factors include obesity, "
         "high sodium diet, lack of exercise, smoking, excessive alcohol, stress, and family history. "
         "Stage 1 hypertension: 130-139/80-89 mmHg. Stage 2: 140+/90+ mmHg. Hypertensive crisis: above 180/120 mmHg. "
         "Treatment includes ACE inhibitors, ARBs, calcium channel blockers, diuretics, and beta-blockers. "
         "Lifestyle modifications: DASH diet, reducing sodium to less than 2300mg/day, regular exercise 150 min/week, "
         "weight management, and stress reduction. Untreated hypertension leads to stroke, heart attack, kidney damage.",
         "hypertension"),

        # HEART DISEASE
        ("Coronary Artery Disease (CAD) is caused by plaque buildup in coronary arteries (atherosclerosis). "
         "Symptoms of a heart attack include chest pain or pressure, shortness of breath, pain radiating to left arm, "
         "jaw, or back, nausea, cold sweats, and lightheadedness. Risk factors: high cholesterol, hypertension, "
         "smoking, diabetes, obesity, sedentary lifestyle, family history. Diagnosis includes ECG, stress test, "
         "coronary angiography, and blood tests for troponin. Treatment: aspirin, statins, beta-blockers, "
         "nitroglycerin, angioplasty with stenting, or coronary artery bypass grafting (CABG). "
         "Prevention: healthy diet, exercise, no smoking, cholesterol management, blood pressure control.",
         "heart_disease"),

        # ASTHMA
        ("Asthma is a chronic respiratory condition causing airway inflammation, narrowing, and excess mucus. "
         "Symptoms: wheezing, shortness of breath, chest tightness, coughing (especially at night or early morning). "
         "Triggers include allergens (dust mites, pollen, pet dander), cold air, exercise, smoke, respiratory infections, "
         "and stress. Diagnosis: spirometry, peak flow meter, methacholine challenge test. "
         "Treatment: Quick-relief inhalers (albuterol/salbutamol) for acute attacks. Long-term controllers: "
         "inhaled corticosteroids (fluticasone, budesonide), long-acting beta agonists (salmeterol, formoterol), "
         "leukotriene modifiers (montelukast). Severe asthma may require oral corticosteroids or biologics. "
         "Asthma action plan: Green zone (well-controlled), Yellow zone (caution), Red zone (emergency).",
         "asthma"),

        # FIRST AID - CPR
        ("Cardiopulmonary Resuscitation (CPR) is a life-saving technique for cardiac arrest. "
         "Steps: 1) Check responsiveness and call emergency services (911). 2) Place person on firm flat surface. "
         "3) Begin chest compressions: push hard and fast in center of chest, 2 inches deep, rate of 100-120/min. "
         "4) After 30 compressions, give 2 rescue breaths (tilt head, lift chin, seal mouth). "
         "5) Continue 30:2 ratio until help arrives or person recovers. Hands-only CPR (no breaths) is also effective. "
         "AED (Automated External Defibrillator): Turn on, follow voice prompts, attach pads to bare chest, "
         "stand clear, press shock if advised. CPR should be started within minutes of cardiac arrest for best outcomes.",
         "first_aid"),

        # FIRST AID - BURNS, FRACTURES, CHOKING
        ("First Aid for Burns: Cool the burn under cool running water for at least 10-20 minutes. "
         "Do NOT use ice, butter, or toothpaste. Cover with sterile non-stick dressing. "
         "First-degree burns: redness only. Second-degree: blisters. Third-degree: white/charred skin (emergency). "
         "First Aid for Fractures: Immobilize the injured area, do not try to realign bones, apply ice wrapped in cloth, "
         "elevate if possible, seek immediate medical attention. Signs: pain, swelling, deformity, inability to move. "
         "First Aid for Choking (Heimlich Maneuver): Stand behind person, make fist above navel, "
         "thrust inward and upward firmly. For infants: 5 back blows + 5 chest thrusts. "
         "For unconscious choking: begin CPR and check airway before each breath.",
         "first_aid"),

        # MEDICATIONS
        ("Common Medications and Their Uses: "
         "Paracetamol (Acetaminophen): pain relief, fever reduction, 500-1000mg every 4-6 hours, max 4g/day. "
         "Ibuprofen: NSAID for pain, inflammation, fever, 200-400mg every 4-6 hours, take with food. "
         "Amoxicillin: antibiotic for bacterial infections (ear, throat, urinary), complete full course. "
         "Omeprazole: proton pump inhibitor for acid reflux, gastritis, peptic ulcers, take before meals. "
         "Metformin: first-line treatment for Type 2 diabetes, take with meals to reduce GI side effects. "
         "Atorvastatin: statin for high cholesterol, take at night for best effect. "
         "Amlodipine: calcium channel blocker for hypertension. "
         "Cetirizine: antihistamine for allergies, may cause drowsiness. "
         "Always check for drug interactions and allergies before taking any medication.",
         "medications"),

        # MENTAL HEALTH
        ("Mental Health - Anxiety and Depression: "
         "Anxiety disorders affect 280 million people worldwide. Symptoms: excessive worry, restlessness, "
         "rapid heartbeat, difficulty concentrating, sleep problems, muscle tension. "
         "Types: Generalized Anxiety Disorder, Panic Disorder, Social Anxiety, OCD, PTSD. "
         "Depression affects 350+ million people. Symptoms: persistent sadness, loss of interest, "
         "fatigue, changes in appetite/weight, sleep disturbances, difficulty concentrating, feelings of worthlessness. "
         "Treatment: CBT (Cognitive Behavioral Therapy), SSRIs (fluoxetine, sertraline), SNRIs (venlafaxine). "
         "Self-help: regular exercise, adequate sleep, social connections, mindfulness meditation, "
         "limiting alcohol/caffeine, journaling. Crisis: If suicidal thoughts, call emergency services immediately.",
         "mental_health"),

        # NUTRITION
        ("Nutrition and Wellness: A balanced diet includes all macronutrients and micronutrients. "
         "Macronutrients: Carbohydrates (45-65% of calories), Proteins (10-35%), Fats (20-35%). "
         "Essential vitamins: A (vision), B-complex (energy), C (immunity), D (bone health), E (antioxidant), K (blood clotting). "
         "Essential minerals: Iron (blood), Calcium (bones), Zinc (immunity), Magnesium (muscles/nerves). "
         "Daily water intake: 2-3 liters for adults. Fiber: 25-30g/day for digestive health. "
         "Mediterranean diet reduces cardiovascular risk. DASH diet for hypertension. "
         "Avoid: excess sugar (max 25g/day women, 36g/day men), trans fats, excessive sodium. "
         "Exercise: 150 minutes moderate aerobic activity per week + strength training 2 days/week.",
         "nutrition"),

        # INFECTIOUS DISEASES
        ("Common Infectious Diseases: "
         "Influenza (Flu): caused by influenza virus, symptoms include fever, cough, body aches, fatigue. "
         "Treatment: rest, fluids, oseltamivir (Tamiflu) within 48 hours. Annual flu vaccine recommended. "
         "COVID-19: caused by SARS-CoV-2, symptoms range from mild (cough, fever, loss of taste) to severe (pneumonia). "
         "Prevention: vaccination, hand hygiene, masks in high-risk settings. "
         "Tuberculosis (TB): bacterial infection by Mycobacterium tuberculosis, affects lungs primarily. "
         "Symptoms: persistent cough 3+ weeks, blood in sputum, night sweats, weight loss. "
         "Treatment: 6-month regimen of isoniazid, rifampicin, pyrazinamide, ethambutol. "
         "Malaria: caused by Plasmodium parasites via mosquito bites. Symptoms: cyclic fever, chills, headache. "
         "Prevention: bed nets, antimalarial drugs. Treatment: artemisinin-based combination therapy.",
         "infectious_diseases"),

        # WOMEN'S HEALTH
        ("Women's Health: "
         "Pregnancy: lasts approximately 40 weeks (3 trimesters). Prenatal care includes folic acid (400mcg/day), "
         "iron supplements, regular ultrasounds, blood pressure monitoring. "
         "Warning signs in pregnancy: vaginal bleeding, severe headache, vision changes, severe abdominal pain. "
         "Common conditions: gestational diabetes, preeclampsia, anemia. "
         "Menstrual Health: normal cycle is 21-35 days. Dysmenorrhea (painful periods) treated with NSAIDs, "
         "hormonal contraceptives. Irregular periods may indicate PCOS, thyroid disorders, or stress. "
         "Breast Cancer screening: mammogram recommended every 1-2 years for women 50+. "
         "Cervical Cancer screening: Pap smear every 3 years (ages 21-65), HPV vaccination recommended.",
         "womens_health"),

        # PEDIATRIC CARE
        ("Pediatric Care and Child Health: "
         "Vaccination schedule: Birth (Hepatitis B), 2 months (DTaP, IPV, Hib, PCV, Rotavirus), "
         "4 months (same + boosters), 6 months (DTaP, PCV, Influenza), 12-15 months (MMR, Varicella, Hepatitis A), "
         "4-6 years (DTaP, IPV, MMR boosters). "
         "Common childhood illnesses: Ear infections (otitis media) - antibiotics if bacterial. "
         "Hand-foot-mouth disease: viral, self-limiting, supportive care. "
         "Chickenpox: caused by varicella-zoster virus, itchy blisters, calamine lotion for relief. "
         "Growth milestones: sitting (6 months), crawling (9 months), walking (12 months), first words (12 months). "
         "Fever in children: paracetamol 15mg/kg every 4-6 hours or ibuprofen 10mg/kg every 6-8 hours. "
         "Seek emergency care for: high fever in infants under 3 months, difficulty breathing, dehydration.",
         "pediatric_care"),

        # ALLERGIES
        ("Allergies and Allergic Reactions: "
         "An allergy is an immune system overreaction to a normally harmless substance (allergen). "
         "Common allergens: pollen, dust mites, pet dander, mold, certain foods (peanuts, shellfish, milk, eggs), "
         "insect stings, latex, medications (penicillin). "
         "Symptoms: sneezing, runny nose, itchy eyes, hives, swelling, shortness of breath. "
         "Anaphylaxis is a severe life-threatening reaction: throat swelling, difficulty breathing, "
         "drop in blood pressure, rapid pulse. Treatment: epinephrine auto-injector (EpiPen) immediately, call 911. "
         "Management: antihistamines (cetirizine, loratadine), nasal corticosteroids, allergen avoidance, "
         "immunotherapy (allergy shots) for long-term desensitization.",
         "allergies"),

        # SKIN CONDITIONS
        ("Common Skin Conditions: "
         "Eczema (Atopic Dermatitis): chronic itchy, inflamed skin. Treatment: moisturizers, topical corticosteroids, "
         "avoiding triggers (harsh soaps, certain fabrics). "
         "Psoriasis: autoimmune condition causing thick, scaly patches. Treatment: topical steroids, "
         "vitamin D analogs, phototherapy, biologics for severe cases. "
         "Acne: caused by clogged pores, bacteria, hormones. Treatment: benzoyl peroxide, salicylic acid, "
         "retinoids, antibiotics for severe cases. Do NOT pop pimples. "
         "Fungal infections (ringworm, athlete's foot): treated with antifungal creams (clotrimazole, terbinafine). "
         "Skin cancer warning signs (ABCDE): Asymmetry, Border irregularity, Color variation, "
         "Diameter >6mm, Evolving size/shape. See a dermatologist for suspicious moles.",
         "skin_conditions"),

        # DIGESTIVE HEALTH
        ("Digestive Health and Gastrointestinal Conditions: "
         "GERD (Acid Reflux): stomach acid flows back into esophagus. Symptoms: heartburn, regurgitation. "
         "Treatment: PPIs (omeprazole), H2 blockers, lifestyle changes (elevate head, avoid late meals). "
         "IBS (Irritable Bowel Syndrome): chronic abdominal pain with diarrhea, constipation, or both. "
         "Management: dietary changes (low-FODMAP diet), stress management, antispasmodics. "
         "Food Poisoning: caused by bacteria (Salmonella, E. coli), viruses, or parasites. "
         "Symptoms: nausea, vomiting, diarrhea within hours to days. Treatment: hydration, rest. "
         "Seek help if: bloody stool, fever above 101.5F, dehydration, symptoms lasting 3+ days. "
         "Appendicitis: sharp pain in lower right abdomen, requires emergency surgery.",
         "digestive_health"),
    ]

    docs = []
    for content, source in knowledge:
        docs.append(Document(page_content=content, metadata={"source": source}))
    return docs