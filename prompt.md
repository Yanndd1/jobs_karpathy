# Exposition à l'IA du marché du travail français

Ce document contient des données structurées sur 147 métiers français issus du répertoire ROME (Répertoire Opérationnel des Métiers et des Emplois) de France Travail, chacun évalué sur une échelle d'exposition à l'IA de 0 à 10 par un LLM. Utilisez ces données pour analyser, questionner et discuter de l'impact de l'IA sur le marché du travail français.

Sources de données : France Travail (ROME), INSEE, DARES

## Méthodologie de scoring

Chaque métier a été évalué sur un axe unique d'Exposition à l'IA de 0 à 10, mesurant dans quelle mesure l'IA va transformer ce métier. Le score prend en compte à la fois l'automatisation directe (l'IA réalisant le travail) et les effets indirects (l'IA rendant les travailleurs si productifs que moins de personnes sont nécessaires).

Un heuristique clé : si le métier peut être exercé entièrement depuis un bureau à domicile sur un ordinateur — écrire, coder, analyser, communiquer — alors l'exposition à l'IA est intrinsèquement élevée (7+). Les spécificités françaises (cadre réglementaire, AI Act européen, droit du travail, métiers réglementés) sont prises en compte.

Repères de calibration :
- 0-1 Minimale : couvreurs, maçons, jardiniers-paysagistes
- 2-3 Faible : électriciens, plombiers, sapeurs-pompiers, aides-soignants
- 4-5 Modérée : infirmiers, policiers, vétérinaires, éducateurs spécialisés
- 6-7 Élevée : enseignants, comptables, journalistes, conseillers bancaires
- 8-9 Très élevée : développeurs, designers graphiques, traducteurs, data analysts
- 10 Maximale : opérateurs de saisie, télévendeurs

## Statistiques agrégées

- Nombre de métiers : 147
- Total emplois : 14 671 500
- Masse salariale annuelle : 442.3 Md€
- Exposition IA moyenne (pondérée par l'emploi) : 4.0/10

### Répartition par niveau d'exposition

| Niveau | Métiers | Emplois | % emplois |
|--------|---------|---------|-----------|
| Minimale (0-1) | 13 | 2.4M | 16.2% |
| Faible (2-3) | 40 | 4.4M | 30.0% |
| Modérée (4-5) | 40 | 4.5M | 30.4% |
| Élevée (6-7) | 30 | 1.9M | 12.8% |
| Très élevée (8-10) | 24 | 1.6M | 10.6% |

### Exposition moyenne par niveau de formation (pondérée)

| Formation | Exposition moy. | Emplois |
|-----------|----------------|---------|

## Les 147 métiers

Triés par exposition à l'IA (décroissant), puis par nombre d'emplois.

### Exposition 10/10 (1 métiers, 0 emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Télévendeurs | ? | ? | ? | Prospection téléphonique scriptée. Les chatbots et voicebots IA remplacent progressivement ce métier. |

### Exposition 9/10 (4 métiers, 90K emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Rédacteurs web | 27 720 € | 42K | ? | Production de contenu générique = exposition maximale aux LLMs. Valeur migre vers la stratégie et la supervision. |
| 2 | Webmasters | 27 720 € | 42K | ? | Production de contenu générique = exposition maximale aux LLMs. Valeur migre vers la stratégie et la supervision. |
| 3 | Secrétaires | 52 200 € | 6K | ? | Modélisation statistique = cœur automatisable par ML spécialisés. Valeur migre vers l'interprétation et la gouvernance. |
| 4 | Opérateurs en centre d'appels | ? | ? | ? | Traitement d'appels standardisés très exposé aux chatbots IA. Seuls les cas complexes nécessitent encore un humain. |

### Exposition 8/10 (19 métiers, 1.5M emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Développeurs informatiques | 46 200 € | 182K | ? | Génération de code par LLMs très avancée (+55% productivité Copilot). Architecture, compréhension produit et jugement système résistent. |
| 2 | Administrateurs systèmes et réseaux | 46 200 € | 182K | ? | Génération de code par LLMs très avancée (+55% productivité Copilot). Architecture, compréhension produit et jugement système résistent. |
| 3 | Ingénieurs en informatique | 46 200 € | 182K | ? | Génération de code par LLMs très avancée (+55% productivité Copilot). Architecture, compréhension produit et jugement système résistent. |
| 4 | Experts en cybersécurité | 46 200 € | 182K | ? | Génération de code par LLMs très avancée (+55% productivité Copilot). Architecture, compréhension produit et jugement système résistent. |
| 5 | Comptables | 31 800 € | 128K | ? | Saisie, déclarations et rapprochements très automatisables. La valeur migre vers le conseil et l'analyse critique. |
| 6 | Experts-comptables | 31 800 € | 128K | ? | Saisie, déclarations et rapprochements très automatisables. La valeur migre vers le conseil et l'analyse critique. |
| 7 | Community managers | 30 000 € | 95K | ? | Production de posts, réponses standardisées et reporting : très automatisables. La stratégie de marque, la gestion de crise et la création de contenu distinctif restent différenciants. ~95 000 CM (INSEE EEC 2024). |
| 8 | Gestionnaires de paie | 33 600 € | 82K | ? | Calcul de paie et déclarations sociales = exposition maximale selon ILO WP140 (ISCO Gradient 4). La valeur migre vers la gestion des cas complexes, la veille réglementaire sociale et le conseil. |
| 9 | Data analysts | 51 360 € | 52K | ? | AutoML et LLMs effectuent les analyses standard. Valeur migre vers la définition du problème et l'interprétation stratégique. |
| 10 | Traders | 48 960 € | 38K | ? | Analyse quantitative et rédaction de rapports = haute automatisabilité. Jugement stratégique et relations client résistent. |
| 11 | Analystes financiers | 48 960 € | 38K | ? | Analyse quantitative et rédaction de rapports = haute automatisabilité. Jugement stratégique et relations client résistent. |
| 12 | Gestionnaires de patrimoine | 50 400 € | 32K | ? | Analyse patrimoniale automatisable, mais conseil personnalisé, relation de confiance et responsabilité fiduciaire freinent la substitution totale. |
| 13 | Responsables marketing | 37 800 € | 28K | ? | Catalogue, SEO, personnalisation très automatisables. Stratégie de marque et expérience client résistent. |
| 14 | Chefs de produit | 37 800 € | 28K | ? | Catalogue, SEO, personnalisation très automatisables. Stratégie de marque et expérience client résistent. |
| 15 | Auditeurs financiers | 44 160 € | 22K | ? | Analyse documentaire et scoring facilement automatisables. L'expertise de jugement dans les cas complexes résiste. |
| 16 | Techniciens audiovisuels | 28 800 € | 18K | ? | Montage automatique (génération de rushes, découpes IA, sous-titrage) : très exposé. L'Adobe Premiere/DaVinci Resolve intègrent déjà l'IA de manière native. La direction éditoriale, le rythme narratif et la post-production de prestige restent différenciants. ~18 000 monteurs (Audiens/CPNEF-AV 2024). |
| 17 | Moniteurs de sport | 28 800 € | 18K | ? | Montage automatique (génération de rushes, découpes IA, sous-titrage) : très exposé. L'Adobe Premiere/DaVinci Resolve intègrent déjà l'IA de manière native. La direction éditoriale, le rythme narratif et la post-production de prestige restent différenciants. ~18 000 monteurs (Audiens/CPNEF-AV 2024). |
| 18 | Traducteurs-interprètes | 27 000 € | 14K | ? | Traduction brute quasi-automatisée par NMT. Valeur sur la post-édition culturelle et la localisation experte. |
| 19 | Manipulateurs en radiologie | 79 800 € | 14K | ? | IA de détection d'anomalies très avancée (AUC > 0.95 sur dépistage). Interprétation finale et actes interventionnels restent médicaux. |

### Exposition 7/10 (15 métiers, 972K emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Conseillers bancaires | 32 160 € | 158K | ? | Analyse financière et conseil patrimonial très exposés aux LLMs et robo-advisors. La relation de confiance personnelle résiste. |
| 2 | Agents d'assurance | 32 160 € | 158K | ? | Analyse financière et conseil patrimonial très exposés aux LLMs et robo-advisors. La relation de confiance personnelle résiste. |
| 3 | Chefs de projets informatiques | 44 160 € | 88K | ? | Planification assistée par IA ; coordination humaine, gestion des risques imprévus et négociation stakeholders résistent. |
| 4 | Techniciens support informatique | 44 160 € | 88K | ? | Planification assistée par IA ; coordination humaine, gestion des risques imprévus et négociation stakeholders résistent. |
| 5 | Avocats | 45 600 € | 79K | ? | Recherche documentaire, rédaction d'actes standard et due diligence : fortement automatisables. Le conseil stratégique, la plaidoirie et les contentieux complexes restent irremplaçables. 79 141 avocats inscrits en janv. 2026 (CNB/Ministère de la Justice). |
| 6 | Contrôleurs de gestion | 41 400 € | 72K | ? | Consolidation et reporting très automatisables. Rôle de business partner et conseil stratégique résistent. |
| 7 | Juristes d'entreprise | 45 600 € | 65K | ? | Revue de contrats, veille réglementaire et rédaction de clauses : automatisables à 60-70%. Le conseil stratégique, la négociation et la gestion des contentieux restent humains. ~65 000 juristes en entreprise (INSEE EEC 2024). |
| 8 | Ingénieurs en mécanique | 42 960 € | 48K | ? | Optimisation de process très exposée aux jumeaux numériques et IA prédictive. Conception système et validation restent humaines. |
| 9 | Techniciens qualité | 42 960 € | 48K | ? | Optimisation de process très exposée aux jumeaux numériques et IA prédictive. Conception système et validation restent humaines. |
| 10 | Designers graphiques | 28 560 € | 48K | ? | Génération d'images automatisée ; direction artistique, identité de marque et jugement esthétique résistent. |
| 11 | Ingénieurs en énergie | 42 960 € | 48K | ? | Optimisation de process très exposée aux jumeaux numériques et IA prédictive. Conception système et validation restent humaines. |
| 12 | Ingénieurs environnement | 42 960 € | 48K | ? | Optimisation de process très exposée aux jumeaux numériques et IA prédictive. Conception système et validation restent humaines. |
| 13 | Greffiers | 27 600 € | 24K | ? | Rédaction de procès-verbaux, saisie d'actes et gestion administrative des dossiers : très exposés à l'automatisation IA. Le rôle d'authentification, la relation aux justiciables et la maîtrise du droit procédural restent différenciants. ~24 000 greffiers fonctionnaires (Ministère de la Justice 2024) · plan de recrutement massif prévu par la LOPJ. |
| 14 | Assistants de direction | ? | ? | ? | Organisation et communication très exposées aux outils IA. Le rôle stratégique de filtrage et de coordination résiste. |
| 15 | Agents des impôts | ? | ? | ? | Contrôle fiscal et traitement de dossiers très automatisables. L'interprétation des situations complexes résiste. |

### Exposition 6/10 (15 métiers, 912K emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Directeurs de magasin | 50 400 € | 180K | ? | Analyse de données, production de slides et reporting : très automatisables. Le diagnostic organisationnel, la relation client et la conduite du changement humain restent des domaines où l'IA augmente sans remplacer. ~180 000 consultants (INSEE EEC 2024). |
| 2 | Agents de transit | 31 800 € | 92K | ? | Optimisation des flux exposée aux algorithmes. Gestion des exceptions, fournisseurs et risques géopolitiques résistent. |
| 3 | Magasiniers | 31 800 € | 92K | ? | Optimisation des flux exposée aux algorithmes. Gestion des exceptions, fournisseurs et risques géopolitiques résistent. |
| 4 | Responsables logistiques | 31 800 € | 92K | ? | Optimisation des flux exposée aux algorithmes. Gestion des exceptions, fournisseurs et risques géopolitiques résistent. |
| 5 | Logisticiens | 31 800 € | 92K | ? | Optimisation des flux exposée aux algorithmes. Gestion des exceptions, fournisseurs et risques géopolitiques résistent. |
| 6 | Déclarants en douane | 31 800 € | 92K | ? | Optimisation des flux exposée aux algorithmes. Gestion des exceptions, fournisseurs et risques géopolitiques résistent. |
| 7 | Responsables des ressources humaines | 48 960 € | 42K | ? | Recrutement et administration RH très exposés. Culture d'entreprise, stratégie humaine et gestion des conflits résistent. |
| 8 | Architectes | 41 400 € | 38K | ? | Conception créative et responsabilité réglementaire résistent ; rendus et variations s'automatisent rapidement. |
| 9 | Géomètres-topographes | 41 400 € | 38K | ? | Conception créative et responsabilité réglementaire résistent ; rendus et variations s'automatisent rapidement. |
| 10 | Urbanistes | 41 400 € | 38K | ? | Conception créative et responsabilité réglementaire résistent ; rendus et variations s'automatisent rapidement. |
| 11 | Journalistes | 29 760 € | 36K | ? | Articles factuels, dépêches et synthèses automatisables. Investigation terrain, récit et fact-checking critique résistent. |
| 12 | Photographes | 28 800 € | 34K | ? | ISCO Gradient 1 selon ILO WP140. La prise de vue reste physique et irremplaçable, mais la retouche, la sélection et la post-production sont sous forte pression. L'ADAGP documente une contraction réelle du marché. |
| 13 | Chargés de communication | 33 600 € | 25K | ? | Rédaction de communiqués, revues de presse et reprises médias : automatisables à 70%. La relation de confiance avec les journalistes, la gestion de crise et la stratégie d'influence restent irremplaçables. ~25 000 attachés de presse (INSEE EEC 2024). |
| 14 | Notaires | 43 200 € | 17K | ? | Actes immobiliers répétitifs, rédaction de clauses standard : exposés aux LLMs spécialisés. Authentification des actes, responsabilité ministerielle et conseil patrimonial complexe restent des fonctions humaines irremplaçables. 17 000 notaires en France (CSN 2024). |
| 15 | Huissiers de justice | 50 400 € | 4K | ? | Issu de la fusion huissiers/commissaires-priseurs (juillet 2022), ce profil hybride combine actes d'exécution forcée, constats et ventes judiciaires. La signification d'actes et la saisie de données sont automatisables. La présence physique, la relation au débiteur et l'autorité de l'officier ministériel restent irremplaçables. ~3 800 commissaires de justice (RSJ 2024). |

### Exposition 5/10 (21 métiers, 2.1M emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Commerciaux terrain | 34 680 € | 242K | ? | Prospection automatisable par IA ; confiance, relation longue durée et négociation complexe résistent. |
| 2 | Acheteurs | 34 680 € | 242K | ? | Prospection automatisable par IA ; confiance, relation longue durée et négociation complexe résistent. |
| 3 | Opérateurs de production | 30 000 € | 195K | ? | Conduite de machines-outils et programmation CFAO partiellement automatisables. La maintenance de premier niveau, le réglage fin et la gestion des aléas de production nécessitent la présence physique. |
| 4 | Usineurs | 30 000 € | 195K | ? | Conduite de machines-outils et programmation CFAO partiellement automatisables. La maintenance de premier niveau, le réglage fin et la gestion des aléas de production nécessitent la présence physique. |
| 5 | Conducteurs de ligne de production | 30 000 € | 195K | ? | Conduite de machines-outils et programmation CFAO partiellement automatisables. La maintenance de premier niveau, le réglage fin et la gestion des aléas de production nécessitent la présence physique. |
| 6 | Agents immobiliers | 29 040 € | 148K | ? | Visites virtuelles et scoring automatique progressent ; négociation et réseau local résistent. |
| 7 | Agents de voyage | 29 040 € | 148K | ? | Visites virtuelles et scoring automatique progressent ; négociation et réseau local résistent. |
| 8 | Formateurs | 35 400 € | 95K | ? | Conception de modules e-learning automatisable. Mais l'animation présentielle, l'adaptation pédagogique en temps réel et l'accompagnement des apprenants en difficulté résistent à l'automatisation. |
| 9 | Chercheurs | 40 800 € | 93K | ? | Production de cours et rédaction d'articles standards très exposées. La recherche originale, la direction de thèse, l'évaluation par les pairs et la transmission du raisonnement scientifique restent profondément humaines. 93 000 enseignants du supérieur (MESR 2023). |
| 10 | Pharmaciens | 46 200 € | 74K | ? | Dispensation automatisée progresse ; conseil patient, pharmacovigilance et gestion clinique résistent. |
| 11 | Opticiens-lunetiers | 46 200 € | 74K | ? | Dispensation automatisée progresse ; conseil patient, pharmacovigilance et gestion clinique résistent. |
| 12 | Préparateurs en pharmacie | 46 200 € | 74K | ? | Dispensation automatisée progresse ; conseil patient, pharmacovigilance et gestion clinique résistent. |
| 13 | Techniciens de laboratoire médical | 46 200 € | 74K | ? | Dispensation automatisée progresse ; conseil patient, pharmacovigilance et gestion clinique résistent. |
| 14 | Diététiciens | 46 200 € | 74K | ? | Dispensation automatisée progresse ; conseil patient, pharmacovigilance et gestion clinique résistent. |
| 15 | Directeurs généraux | 66 000 € | 38K | ? | Planification et suivi de planning automatisables. La gestion des parties prenantes, la résolution de conflits et l'arbitrage stratégique des projets nécessitent le jugement et l'autorité humaine. |
| 16 | Directeurs financiers | 66 000 € | 38K | ? | Planification et suivi de planning automatisables. La gestion des parties prenantes, la résolution de conflits et l'arbitrage stratégique des projets nécessitent le jugement et l'autorité humaine. |
| 17 | Techniciens en électronique | 34 200 € | 38K | ? | Programmation d'automates partiellement assistée par IA ; intégration terrain et validation système résistent. |
| 18 | Techniciens télécoms | 34 200 € | 38K | ? | Programmation d'automates partiellement assistée par IA ; intégration terrain et validation système résistent. |
| 19 | Techniciens en énergie renouvelable | 34 200 € | 38K | ? | Programmation d'automates partiellement assistée par IA ; intégration terrain et validation système résistent. |
| 20 | Guides touristiques | ? | ? | ? | Audioguides et visites virtuelles IA progressent. Le contact humain, l'improvisation et la narration vivante résistent. |
| 21 | Attachés territoriaux | ? | ? | ? | Administration et rédaction de rapports exposées. La connaissance du terrain local et la médiation politique résistent. |

### Exposition 4/10 (19 métiers, 2.3M emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Enseignants du secondaire | 32 160 € | 530K | ? | Production de cours, correction de copies : automatisables. L'animation pédagogique, la relation éducative, la gestion des difficultés d'apprentissage et la mission de socialisation restent irremplaçables. 530 000 enseignants du 2nd degré (DEPP Panorama 2024-2025). |
| 2 | Enseignants du primaire | 28 560 € | 370K | ? | Tuteurs IA personnalisés (Khan Academy, Khanmigo) progressent mais la relation éducative, la gestion de classe, la socialisation précoce et l'adaptation aux besoins individuels restent irremplaçables. 370 500 professeurs des écoles en France (DEPP 2024). |
| 3 | Conducteurs routiers | 24 960 € | 278K | ? | Conduite autonome progresse (L4 en zone contrôlée) mais contexte réglementaire FR maintient un humain à moyen terme. |
| 4 | Livreurs | 24 960 € | 278K | ? | Conduite autonome progresse (L4 en zone contrôlée) mais contexte réglementaire FR maintient un humain à moyen terme. |
| 5 | Policiers | 27 000 € | 155K | ? | Intervention terrain, médiation, décision en urgence · IA assiste sans remplacer l'officier. |
| 6 | Gendarmes | 27 000 € | 155K | ? | Intervention terrain, médiation, décision en urgence · IA assiste sans remplacer l'officier. |
| 7 | Médecins généralistes | 64 080 € | 96K | ? | Diagnostic augmenté par IA, mais relation thérapeutique, gestion de l'incertitude et empathie restent irremplaçables. |
| 8 | Réceptionnistes d'hôtel | 22 080 € | 62K | ? | Check-in digitaux progressent ; relation et service personnalisés haut-de-gamme restent humains. |
| 9 | Agents d'accueil | 22 080 € | 62K | ? | Check-in digitaux progressent ; relation et service personnalisés haut-de-gamme restent humains. |
| 10 | Vendeurs en magasin | 27 000 € | 58K | ? | Configurateurs en ligne progressent mais la découverte physique et la négociation restent essentielles. |
| 11 | Conducteurs de travaux | 39 360 € | 52K | ? | Coordination multi-acteurs et gestion des aléas de chantier freinent l'automatisation. Responsabilité juridique maintient l'humain. |
| 12 | Conducteurs de bus | 39 360 € | 52K | ? | Coordination multi-acteurs et gestion des aléas de chantier freinent l'automatisation. Responsabilité juridique maintient l'humain. |
| 13 | Conducteurs de train | 39 360 € | 52K | ? | Coordination multi-acteurs et gestion des aléas de chantier freinent l'automatisation. Responsabilité juridique maintient l'humain. |
| 14 | Ingénieurs BTP | 39 360 € | 52K | ? | Coordination multi-acteurs et gestion des aléas de chantier freinent l'automatisation. Responsabilité juridique maintient l'humain. |
| 15 | Chirurgiens-dentistes | 50 400 € | 40K | ? | Gestes cliniques et chirurgicaux irremplaçables. L'IA progresse sur la détection des caries et pathologies (radiographies, CBCT) mais n'effectue pas les soins. 40 000 chirurgiens-dentistes (DREES/RPPS 2024). |
| 16 | Vétérinaires | 38 400 € | 20K | ? | Examen clinique et chirurgie : irremplaçables. L'IA progresse sur l'imagerie (radio, écho) et le diagnostic différentiel assisté. 20 000 vétérinaires en France (ONVS 2024). |
| 17 | Bibliothécaires | 38 400 € | 12K | ? | Le jugement curatorial (authenticité, provenance, signification culturelle) est une expertise humaine irréductible. L'IA augmente la numérisation et la médiation mais ne remplace pas l'expertise scientifique. |
| 18 | Opérateurs de saisie | 38 400 € | 12K | ? | Le jugement curatorial (authenticité, provenance, signification culturelle) est une expertise humaine irréductible. L'IA augmente la numérisation et la médiation mais ne remplace pas l'expertise scientifique. |
| 19 | Conseillers en insertion professionnelle | 30 000 € | 11K | ? | Les outils d'orientation algorithmiques (Parcoursup, Mon Master) se développent mais l'accompagnement psychologique individualisé, la détection des troubles et la relation de confiance restent irremplaçables. ~11 000 PsyEN en France (MEN 2024). |

### Exposition 3/10 (22 métiers, 2.4M emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Infirmiers en soins généraux | 28 080 € | 580K | ? | Soins directs, gestes techniques, soutien psychologique · IA assiste l'administratif sans remplacer le soin. |
| 2 | Agriculteurs | 21 840 € | 165K | ? | Présence terrain et conduite d'engins limitent l'automatisation. Les outils d'aide à la décision progressent mais restent en appui. |
| 3 | Ingénieurs agronomes | 21 840 € | 165K | ? | Présence terrain et conduite d'engins limitent l'automatisation. Les outils d'aide à la décision progressent mais restent en appui. |
| 4 | Mécaniciens automobiles | 24 000 € | 120K | ? | Diagnostic et réparation physique sur véhicule : difficile à automatiser. Les outils OBD/IA assistent sans remplacer la compétence terrain. La transition VE crée une demande de nouvelles compétences critiques. 120 000 mécaniciens (ANFA/INSEE 2024). |
| 5 | Carrossiers | 24 000 € | 120K | ? | Diagnostic et réparation physique sur véhicule : difficile à automatiser. Les outils OBD/IA assistent sans remplacer la compétence terrain. La transition VE crée une demande de nouvelles compétences critiques. 120 000 mécaniciens (ANFA/INSEE 2024). |
| 6 | Mécaniciens aéronautiques | 24 000 € | 120K | ? | Diagnostic et réparation physique sur véhicule : difficile à automatiser. Les outils OBD/IA assistent sans remplacer la compétence terrain. La transition VE crée une demande de nouvelles compétences critiques. 120 000 mécaniciens (ANFA/INSEE 2024). |
| 7 | Kinésithérapeutes | 33 600 € | 105K | ? | Le toucher thérapeutique et l'adaptation en temps réel à la douleur sont non-substituables. Les exosquelettes et applications de téléréhabilitation assistent sans remplacer. 105 000 kinésithérapeutes (DREES/RPPS 2024). |
| 8 | Éducateurs spécialisés | 24 600 € | 105K | ? | Relation éducative, accompagnement individualisé et médiation résistent à l'automatisation. |
| 9 | Animateurs socioculturels | 24 600 € | 105K | ? | Relation éducative, accompagnement individualisé et médiation résistent à l'automatisation. |
| 10 | Moniteurs-éducateurs | 24 600 € | 105K | ? | Relation éducative, accompagnement individualisé et médiation résistent à l'automatisation. |
| 11 | Orthophonistes | 33 600 € | 105K | ? | Le toucher thérapeutique et l'adaptation en temps réel à la douleur sont non-substituables. Les exosquelettes et applications de téléréhabilitation assistent sans remplacer. 105 000 kinésithérapeutes (DREES/RPPS 2024). |
| 12 | Ergothérapeutes | 33 600 € | 105K | ? | Le toucher thérapeutique et l'adaptation en temps réel à la douleur sont non-substituables. Les exosquelettes et applications de téléréhabilitation assistent sans remplacer. 105 000 kinésithérapeutes (DREES/RPPS 2024). |
| 13 | Techniciens de maintenance industrielle | 26 160 € | 92K | ? | Diagnostic et intervention physique restent manuels. La maintenance prédictive assiste sans remplacer. |
| 14 | Techniciens en traitement des eaux | 26 160 € | 92K | ? | Diagnostic et intervention physique restent manuels. La maintenance prédictive assiste sans remplacer. |
| 15 | Techniciens frigoristes | 26 160 € | 92K | ? | Diagnostic et intervention physique restent manuels. La maintenance prédictive assiste sans remplacer. |
| 16 | Psychologues | 26 400 € | 80K | ? | La relation thérapeutique, le transfert et la formulation clinique restent irremplaçables. Les chatbots CBT assurent un premier niveau d'écoute mais ne se substituent pas au suivi psychologique. 80 000 psychologues inscrits (DREES/RPPS 2024). |
| 17 | Comédiens | 23 400 € | 65K | ? | ILO WP140 classe les acteurs en Minimal Exposure (0.31). La présence physique, la performance incarnée et l'émotion en temps réel sont irremplaçables sur scène. Risque réel sur le doublage, les synthèses vocales et les doublures numériques (deepfakes). |
| 18 | Sages-femmes | 28 800 € | 24K | ? | Accompagnement de la naissance, surveillance du travail et décision clinique en temps réel : non substituables. L'IA assiste le monitoring foetal (CTG) et la détection d'anomalies sans remplacer le jugement. 24 000 sages-femmes (DREES/RPPS 2024). |
| 19 | Musiciens | 21 360 € | 22K | ? | Performance live et interprétation émotionnelle · l'IA génère mais ne performe pas. Valeur sur le live et la pédagogie. |
| 20 | Pilotes d'avion | 86 400 € | 14K | ? | Automatisation forte en vol nominal. Décision d'urgence, gestion CRM et responsabilité réglementaire maintiennent l'humain. |
| 21 | Agents de sécurité | ? | ? | ? | Surveillance terrain et intervention physique limitent l'automatisation. La vidéosurveillance IA progresse mais ne remplace pas la présence humaine. |
| 22 | Conducteurs d'engins de chantier | ? | ? | ? | Conduite d'engins en milieu de chantier variable. La téléopération progresse mais le contexte imprévisible freine l'automatisation. |

### Exposition 2/10 (18 métiers, 2.0M emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Aides-soignants | 22 680 € | 355K | ? | Soin direct, nursing et relationnel humain · non substituable par aucun modèle actuel. |
| 2 | Caissiers | 21 360 € | 218K | ? | Dextérité, créativité culinaire et adaptation en temps réel · automatisation anecdotique hors fast-food. |
| 3 | Cuisiniers | 21 360 € | 218K | ? | Dextérité, créativité culinaire et adaptation en temps réel · automatisation anecdotique hors fast-food. |
| 4 | Boulangers-pâtissiers | 21 360 € | 218K | ? | Dextérité, créativité culinaire et adaptation en temps réel · automatisation anecdotique hors fast-food. |
| 5 | Bouchers | 21 360 € | 218K | ? | Dextérité, créativité culinaire et adaptation en temps réel · automatisation anecdotique hors fast-food. |
| 6 | Chefs de cuisine | 21 360 € | 218K | ? | Dextérité, créativité culinaire et adaptation en temps réel · automatisation anecdotique hors fast-food. |
| 7 | Assistants de service social | 25 800 € | 145K | ? | L'accompagnement social individuel, la gestion des crises et la médiation familiale reposent entièrement sur la relation humaine, le jugement contextuel et la confiance. ILO WP140 classifie ces métiers Not Exposed. |
| 8 | Électriciens du bâtiment | 24 960 € | 112K | ? | Intervention physique et diagnostic terrain restent manuels. Pénurie de compétences persistante. |
| 9 | Éleveurs | 21 000 € | 98K | ? | Robots de traite existent mais la gestion du troupeau reste très humaine. |
| 10 | Soudeurs | 26 160 € | 82K | ? | Cobots progressent sur les soudures répétitives ; contextes variables et positions complexes restent manuels. |
| 11 | Chaudronniers | 26 160 € | 82K | ? | Cobots progressent sur les soudures répétitives ; contextes variables et positions complexes restent manuels. |
| 12 | Ouvriers viticoles | 19 800 € | 52K | ? | Travail physique saisonnier et grande variabilité des produits limitent l'automatisation. |
| 13 | Serveurs de restaurant | ? | ? | ? | Service en salle requiert présence physique, adaptation et contact humain. Automatisation anecdotique hors restauration rapide. |
| 14 | Plombiers-chauffagistes | ? | ? | ? | Intervention physique en milieu non structuré. Diagnostic et réparation manuels. Forte pénurie de main-d'œuvre. |
| 15 | Sapeurs-pompiers | ? | ? | ? | Intervention d'urgence physique en milieu dangereux. L'IA assiste la détection d'incendie et la logistique sans remplacer l'intervention. |
| 16 | Ambulanciers | ? | ? | ? | Transport sanitaire et premiers soins requièrent une présence physique et une réactivité humaine. |
| 17 | Pêcheurs | ? | ? | ? | Travail physique en mer, conditions imprévisibles. La technologie assiste la navigation et la détection mais pas la pêche elle-même. |
| 18 | Entraîneurs sportifs | ? | ? | ? | Coaching physique, motivation et adaptation en temps réel. Les applications fitness IA assistent mais ne remplacent pas. |

### Exposition 1/10 (13 métiers, 2.4M emplois)

| # | Métier | Salaire | Emplois | Formation | Explication |
|---|--------|---------|---------|-----------|-------------|
| 1 | Assistants maternels | 18 960 € | 695K | ? | Présence physique, empathie et adaptation permanente · non-automatisable avec les technologies actuelles. |
| 2 | Aides à domicile | 18 960 € | 695K | ? | Présence physique, empathie et adaptation permanente · non-automatisable avec les technologies actuelles. |
| 3 | Maçons | 23 760 € | 128K | ? | Travail physique en milieu non structuré · très difficile à automatiser. Contexte variable de chaque chantier. |
| 4 | Peintres en bâtiment | 23 760 € | 128K | ? | Travail physique en milieu non structuré · très difficile à automatiser. Contexte variable de chaque chantier. |
| 5 | Charpentiers | 23 760 € | 128K | ? | Travail physique en milieu non structuré · très difficile à automatiser. Contexte variable de chaque chantier. |
| 6 | Couvreurs | 23 760 € | 128K | ? | Travail physique en milieu non structuré · très difficile à automatiser. Contexte variable de chaque chantier. |
| 7 | Menuisiers | 23 760 € | 128K | ? | Travail physique en milieu non structuré · très difficile à automatiser. Contexte variable de chaque chantier. |
| 8 | Carreleurs | 23 760 € | 128K | ? | Travail physique en milieu non structuré · très difficile à automatiser. Contexte variable de chaque chantier. |
| 9 | Coiffeurs | 20 400 € | 110K | ? | Contact physique, geste technique personnalisé et relation de confiance : exposition minimale à l'IA. Les outils de visualisation (essayage virtuel) assistent le conseil sans substituer la prestation. 110 000 coiffeurs (UNEC/INSEE 2024). |
| 10 | Esthéticiens | 20 400 € | 110K | ? | Contact physique, geste technique personnalisé et relation de confiance : exposition minimale à l'IA. Les outils de visualisation (essayage virtuel) assistent le conseil sans substituer la prestation. 110 000 coiffeurs (UNEC/INSEE 2024). |
| 11 | Jardiniers-paysagistes | ? | ? | ? | Travail physique en extérieur, adaptation constante au terrain et au vivant. Exposition minimale. |
| 12 | Agents d'entretien | ? | ? | ? | Travail physique de nettoyage. Robots aspirateurs existent mais ne couvrent pas le spectre complet des tâches. |
| 13 | Agents de propreté urbaine | ? | ? | ? | Travail physique en extérieur, conditions variables. Automatisation très limitée en milieu urbain. |
