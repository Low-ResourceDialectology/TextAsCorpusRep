# -*- coding: utf-8 -*-
# Python Script to translate NLLB Seed data as pivot data for MTACR project.
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

import json
import logging
import os
import subprocess
import sys

import utilities as util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


def main(input_path, output_path, script_mode, languages):

	# ===========================================
	# Using Google Translate Command Line API https://manpages.ubuntu.com/manpages/focal/man1/trans.1.html
	# ===========================================
	"""
	input_file = ./../data/input/eng_Latn
	output_file = ./../data/automatic/nllb.deu | ./../data/automatic/nllb.kur | ...
	language_code = de | ku | ... 
	"""
	def translation_via_google_translate(input_file, output_file, language_code):
		# trans -e google file://./../data/experiment_poc_nov_2023/source/2023AlamCODET-German/Standard.deu >> ./../data/experiment_poc_nov_2023/target/google/2023AlamCODET-German/Standard.deu.eng -t en
		print(f'trans -e google file://{input_file} >> {output_file} -t {language_code}')
		command = f'trans -e google file://{input_file} >> {output_file} -t {language_code}'
		subprocess.run(command, shell = True, executable="/bin/bash")

	# ===========================================
	# Using nllb-200-distilled-600M 
	# Based on Sina's NLLB_monolithic Colab Code: https://colab.research.google.com/drive/1_MywMGDSuge3oxrkZEwPWHV-2ifQZq1U
	# ===========================================
	"""
	input_file = ./../data/input/eng_Latn
	output_file = ./../data/automatic/nllb.deu | ./../data/automatic/nllb.kur | ...
	language_code = de | ku | ... 
	"""
	# TODO: Once at home with powerful computer again ;)
	def translation_via_nllb_200(input_path, output_path, language):
		tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
		model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M").cuda()
		model.device

		# Translate the file from English, into target language
		# Get translater model based on target language
		if language == "kur":
			current_translator = pipeline('translation', 
							model=model, 
							tokenizer=tokenizer, 
							src_lang='eng_Latn', 
							tgt_lang='kmr_Latn', 
							max_length = 550, 
							device=model.device, 
							num_beams=3, 
							early_stopping=True)
			#input_file_ending = ".kmr"

		# For all text files in current directory
		for filename in os.listdir(input_path):
			input_textfile = os.path.join(input_path, filename)
			output_textfile = os.path.join(output_path, language)
			
			# Check if it is a file
			if os.path.isfile(input_textfile):
				#print(input_textfile)

				# Check if text is already translated (called "Reference")
				#if os.path.basename(input_textfile).split(".")[0] == "Reference":
				#	print("Reference file detected, moving to output directory without translating.")
				#	os.rename(input_textfile, output_textfile)

				# Is the file not a Reference, translate it into English
				#else:
				# Read the file
				with open(input_textfile, "r") as f:
					text = f.read().splitlines()

				# Print length of input file
				print("Input (source) length: ", len(text))

				# For current target language text:
				trans_text = current_translator(text)
				trans_text = [i["translation_text"] for i in trans_text]
				#print(text)
				#print(trans_text)

				# Print length of translation
				print("Output (target) length: ", len(trans_text))

				# Save the translation
				with open(output_textfile, "w") as f:
					f.write("\n".join(trans_text))
					#os.rename(input_textfile+".en", output_textfile+".en")

			else:
				print("ERROR: Not a text file: "+str(input_textfile))


	# ===========================================
	# Translate NLLB-Seed data automatically
	# ===========================================
	def translate_nllb_seed(input_path, output_path, filename, languages, script_mode):
		
		for language in languages:
			logging.debug(f'Translating NLLB Seed into: {language}')
			if language == "vie":
				language_code = "vi"
			elif language == "deu":
				language_code = "de"
			elif language == "kur":
				language_code = "ku"
			elif language == "zho":
				language_code = "zh-CN"
			elif language == "fra":
				language_code = "fr"
			elif language == "amh":
				language_code = "am"
			elif language == "aze":
				language_code = "az"
			elif language == "spa":
				language_code = "es"
			elif language == "tur":
				language_code = "tr"
			elif language == "ukr":
				language_code = "uk"
			elif language == "rus":
				language_code = "ru"

			if "googleTranslate" in script_mode:
				translation_via_google_translate(input_path+filename, output_path+"nllb_gt."+language, language_code)
			if "nllb200" in script_mode:
				translation_via_nllb_200(input_path, output_path+"nllb_nllb.", language)


	filename = "eng_Latn"
	translate_nllb_seed(input_path, output_path, filename, languages, script_mode)
	


# Language Codes supported by the Google Translate Command Line API
#
#  ┌───────────────────────┬───────────────────────┬───────────────────────┐
#  │ Afrikaans      -   af │ Hebrew         -   he │ Portuguese     -   pt │
#  │ Albanian       -   sq │ Hill Mari      -  mrj │ Punjabi        -   pa │
#  │ Amharic        -   am │ Hindi          -   hi │ Querétaro Otomi-  otq │
#  │ Arabic         -   ar │ Hmong          -  hmn │ Romanian       -   ro │
#  │ Armenian       -   hy │ Hmong Daw      -  mww │ Russian        -   ru │
#  │ Azerbaijani    -   az │ Hungarian      -   hu │ Samoan         -   sm │
#  │ Bashkir        -   ba │ Icelandic      -   is │ Scots Gaelic   -   gd │
#  │ Basque         -   eu │ Igbo           -   ig │ Serbian (Cyr...-sr-Cyrl
#  │ Belarusian     -   be │ Indonesian     -   id │ Serbian (Latin)-sr-Latn
#  │ Bengali        -   bn │ Irish          -   ga │ Sesotho        -   st │
#  │ Bosnian        -   bs │ Italian        -   it │ Shona          -   sn │
#  │ Bulgarian      -   bg │ Japanese       -   ja │ Sindhi         -   sd │
#  │ Cantonese      -  yue │ Javanese       -   jv │ Sinhala        -   si │
#  │ Catalan        -   ca │ Kannada        -   kn │ Slovak         -   sk │
#  │ Cebuano        -  ceb │ Kazakh         -   kk │ Slovenian      -   sl │
#  │ Chichewa       -   ny │ Khmer          -   km │ Somali         -   so │
#  │ Chinese Simp...- zh-CN│ Klingon        -  tlh │ Spanish        -   es │
#  │ Chinese Trad...- zh-TW│ Klingon (pIqaD)tlh-Qaak Sundanese      -   su │
#  │ Corsican       -   co │ Korean         -   ko │ Swahili        -   sw │
#  │ Croatian       -   hr │ Kurdish        -   ku │ Swedish        -   sv │
#  │ Czech          -   cs │ Kyrgyz         -   ky │ Tahitian       -   ty │
#  │ Danish         -   da │ Lao            -   lo │ Tajik          -   tg │
#  │ Dutch          -   nl │ Latin          -   la │ Tamil          -   ta │
#  │ Eastern Mari   -  mhr │ Latvian        -   lv │ Tatar          -   tt │
#  │ Emoji          -  emj │ Lithuanian     -   lt │ Telugu         -   te │
#  │ English        -   en │ Luxembourgish  -   lb │ Thai           -   th │
#  │ Esperanto      -   eo │ Macedonian     -   mk │ Tongan         -   to │
#  │ Estonian       -   et │ Malagasy       -   mg │ Turkish        -   tr │
#  │ Fijian         -   fj │ Malay          -   ms │ Udmurt         -  udm │
#  │ Filipino       -   tl │ Malayalam      -   ml │ Ukrainian      -   uk │
#  │ Finnish        -   fi │ Maltese        -   mt │ Urdu           -   ur │
#  │ French         -   fr │ Maori          -   mi │ Uzbek          -   uz │
#  │ Frisian        -   fy │ Marathi        -   mr │ Vietnamese     -   vi │
#  │ Galician       -   gl │ Mongolian      -   mn │ Welsh          -   cy │
#  │ Georgian       -   ka │ Myanmar        -   my │ Xhosa          -   xh │
#  │ German         -   de │ Nepali         -   ne │ Yiddish        -   yi │
#  │ Greek          -   el │ Norwegian      -   no │ Yoruba         -   yo │
#  │ Gujarati       -   gu │ Papiamento     -  pap │ Yucatec Maya   -  yua │
#  │ Haitian Creole -   ht │ Pashto         -   ps │ Zulu           -   zu │
#  │ Hausa          -   ha │ Persian        -   fa │                       │
#  │ Hawaiian       -  haw │ Polish         -   pl │                       │
#  └───────────────────────┴───────────────────────┴───────────────────────┘

"""
Google Translate Command Line API throwing some shade at NLLB's seed sentences? XD


Did you mean: The first several generations of Fishes were Dunkard ministers.
Did you mean: Note: Source misspells Keaton's frequent appellation as "Great Stone Face".
Did you mean: Confined to a hospital during his final days, Keaton was restless and pacing the room endlessly, desiring to return home.
Did you mean: Pickford left Biography in December 1910.
Did you mean: Pickford left the stage to join Zuko's roster of stars.
Did you mean: She demanded (and received) these powers in 1916, when she was under contract to Zuko's Famous Players in Famous Plays (later Paramount).
Did you mean: Swanson and her husband first got to know John Lennon and Yoko Ono because they were fans of Duffy's work.
Did you mean: In 1912, Alfred become an Episcopalian.
Did you mean: He first met George Gershwin, who was working as a song plugger for Jerome H. Remick music publishing company, in 1916.
Did you mean: Six out of the nine Astaire–Rogers musicals became the biggest money makers for RKO; all of the films brought a certain prestige and artistry that all studios coveted at the time.
Did you mean: Tracy received top billing, but Bogart appeared on the film posters.
Did you mean: Bogart is reported to have been responsible for the notion that Rick Blaine should be portrayed as a chess player, a metaphor for the relationships be maintained with friends, enemies, and allies.
Did you mean: Bogart went on United Service Organizations and War Bond tours with Method in 1943 and 1944, making arduous trips to Italy and North Africa (including Casablanca).
Did you mean: She Liked my undies in darkest Africa."
Did you mean: Coincidentally, the psychiatrist know a doctor friend of Brando.
Did you mean: Another defence of history from postmodernist criticism was the Australian historian Keith Windschuttle 1994 book, The Killing of History.
Did you mean: Historical emissions can occur in many ways and can have a profound effect on historical records.
Did you mean: The Moon is formed around this time probably due to a protoplanet collision into Earth.
Did you mean: Gradually, life expands to land and familiar forms of plants, animals and fungi begin appearing, including annelids, insects and reptiles, hence the son's name, which means "visible life".
Did you mean: Plants evolved seeds, which dramatically accelerated the spread on land, around this time (by approximately 360 Ma).
Did you mean: This was by far the deadliest extinction ever, with about 57% of all families and 83% of all general killed.
Did you mean: The Neolithic saw the Agricultural Revolution begin, between 10,000 and 5000 BCE, in the Near East Fertile Crescent.
Did you mean: These were Daoism, Legalism, and Confucianism.
Did you mean: Arab domination of the region ended in the mid-11th century with the arrival of the Seljuk Turks, migrating south from the Turkic homelands in Central Asia.
Did you mean: It has developed an advanced monetary economics by 1000 CE.
Did you mean: Russia made incursions into the northwest coast of North America, with a first colony in present-day Alaska in 1784, and the outpost of Fort Ross in present-day California in 1812.
Did you mean: By World War I, cheap hardcover reprints has become popular.
Did you mean: Many countries had both timber and stone castles, however Denmark had few queries and as a result most of its castles are earth and timber affairs, or later on built from brick.
Did you mean: Trade was allowed only in the cities when the mercantilist ideology has got the upper hand, and the burghers had the exclusive right to conduct commerce within the framework of guilds.
Did you mean: In 1815, when the Netherlands were united with Belgium and Luxembourg, the States General were divided into two chambers: the First Chamber and the Second Chamber.
Did you mean: The four major estates were: nobility (dvorianstvo), clergy, rural dwellers, and urban dwellers, with a more detailed stratification therein.
Did you mean: Hitler distrusted capitalism for being unreliable due to its egoism, and he preferred a state-directed economy that is subordinated to the interests of the Volk.
Did you mean: The succeeding Nerva-Antonine Dynasty, ruling for most of the 2nd century, stabilised the Empire.
Did you mean: In the following centuries, independent city-states of Greece, especially Athens, developed the polis, an association of male land owning citizens who collectively constitute the city.
Did you mean: Western Europe's largest capitals (London and Paris) benefited from the growth of commerce following the emergence of an Atlantic trade.
Did you mean: Aerial particles increase rainfall by 5–10%.
Did you mean: In 1791, a map of France by J. L. Dupain-Trial use contour lines at 20-metre intervals, hachures, spot-heights and a vertical section.
Did you mean: Acid precipitation is indicated on maps with isoplays.
Did you mean: In interpreting radar images, an isotope is a line of equal Doppler velocity, and an isoechoic is a line of equal radar reflectivity.
Did you mean: Coordinates on a map are usually in terms northingS and easting E offsets relative to a specified origin.
Did you mean: David Schneider's cultural analysis of American kinship has proven equally influential.
Did you mean: The shift can be traced back to the 1960s, with the reassessment of kinship's basic principles offered by Edmund Leach, Rodney Needham, David Schneider, and others.
Did you mean: He feels, in fact, that the exemplary center idea is one of linguistic anthropology three most important findings.
Did you mean: Rites, rituals, and other evidence of religion have long been an interest and are sometimes central to ethnographic, especially when conducted in public where visiting anthropologists can see them.
Did you mean: Land claims were made through symbolic "rituals of discovery" that were performed to illustrate the colonizing nations legal claim to the land.
Did you mean: Not far from the Mutirikwi river, the Monomotapa kings built the Great Zimbabwe complex, a civilisation ancestral to the Kalanga people.
Did you mean: He records the name of the Basque language as euskara.
Did you mean: Navarre has a separate statute of autonomy, a contentious arrangement designed during Spanish transition to democracy (the Mejoramiento, an 'upgrade' of its previous status during dictatorship).
Did you mean: It is unclear if these Germany speak a Germanic language, and they may have been Celtic speakers instead.
Did you mean: Hermione or Hermione in the interior, included the Suevi, the Hermunduri, the Chatti, the Cherusci according to Pliny.
Did you mean: On the other hand, Tacitus wrote in the same passage that some believe that there are other groups which are just as old as these three, including "the Marsi, Gambrivii, Suevi, Vandelli".
Did you mean: They created the Mandate of Heaven to explain their right to assume role and presumed that the only way to hold the mandate was to rule well in the eyes of Heaven.
Did you mean: During a 1976 meeting of the Sociobiology Study Group, as reported by Ulica Segerstråle, Chomsky argued for the importance of a socio biologically informed notion of human nature.
Did you mean: Smith wrote that the "real price of everything ... is the toil and trouble of acquiring it".
Did you mean: Such aggregates include national income and output, the unemployment rate, and price inflation and sub aggregates like total consumption and investment spending and their components.
Did you mean: The purines include guanine (G) and adenine (A) whereas the pyrimidines consist of cytosine (TO), uracil (U), and thymine (T).
Did you mean: According to the first law of thermodynamics, energy is conserved, i.t., cannot be created or destroyed.
Did you mean: During anaerobic glycolysis, NAD+ regenerated when pairs of hydrogen combine with pyruvate to form lactate.
Did you mean: Most nonvascular plants are terrestrial, with a few living in freshwater environments and non living in the oceans.
Did you mean: Paleobotanist study ancient plants in the fossil record to provide information about the evolutionary history of plants.
Did you mean: These groups have since been revised to improve consistency with the Darwinian principle of common descent.
Did you mean: One of the classic cases in North America is that of the protected northern spotted owl which hybridised with the unprotected California spotted owl and the barred owl; this has led to legal debates.
Did you mean: In other systems, such as Lynn Margulis's system of five kingdoms, the plants included just the land plants (Embryophytes), and Protoctista has a broader definition.
Did you mean: The generation of new genes can also involve small parts of several genes being duplicated, with these fragments then recombined to form new combinations with new functions.
Did you mean: Contemporary thinking about the role of mutation bias reflects a different theory from that of Haldane and Fisher.
Did you mean: This is especially the case in the more macroscopic fields of science (i.n. psychology, physical cosmology).
Did you mean: Science policy that deals with the entire domain of issues that involve the natural sciences.
Did you mean: Nature and wilderness have been important subjects in various eras of world history.
Did you mean: Background research would include, for example, geographical or procedural research.
Did you mean: Even taking a plane from New York to Paris is an experiment that tests the aerodynamic hypotheses used for constructing the plane.
Did you mean: Consequently, the conduct of abduction, which is chiefly a question of heuristic and is the first question of heretic, is to be governed by economical considerations."
Did you mean: In Proofs and Refutations, Lakatos have several basic rules for finding proofs and counterexamples to conjectures.
Did you mean: On the largest scale, cosmobiology concerns life in the universe over cosmological times.
Did you mean: Over the years, science fiction communicate scientific ideas, imagined a wide range of possibilities, and influenced public interest in and perspectives of extraterrestrial life.
Did you mean: It is believed by futurists that nanotechnology will allow humans to 'manipulate matter at the molecular and atomic scale.'
Did you mean: The six classical simple machines were known in the ancient Near East.
Did you mean: In this process, carbohydrates in the grains broken down into alcohols, such as ethanol.
Did you mean: 10% of the world's croplands were planted with GM crops in 2010.
Did you mean: This process is also called "research cloning" of "therapeutic cloning".
Did you mean: There are proposals to remove the virulence genes from viruses to create vaccines.
Did you mean: An attractive target for biological control are mosquitoes, vectors for a range of deadly diseases, including malaria, yellow fever and dengue fever.
Did you mean: Unlike mutagenesis, genetic engineering allows targeted removal without disrupting other genes in the organism.
Did you mean: Some genes do not work well in bacteria, so yeast, insect cells for mammalian cells can also be used.
Did you mean: Nanotechnology, also shortened to nanotec, is the use of matter on an atomic, molecular, and supramolecular scale for industrial purposes.
Did you mean: If the catalyst surface area that is exposed to the exhaust fumes is maximized, efficiency of the catalyst is maximized.
Did you mean: The, Pierre Curie and Marie Curie began investigating the phenomenon.
Did you mean: For the hundreds place, they then used the symbols for the units place, and so on.
Did you mean: The fundamental theorem of arithmetic was first proved by Carl Friedrich Gauss.
Did you mean: This study is sometimes known as algorithm.
Did you mean: The later Middle English terms "adding" and "adding" were popularized by Chaucer.
Did you mean: To subtract, the operator has to use the Pascal's calculator complement, which requires as many steps as an addition.
Did you mean: The Euclidean algorithm was first described numerically and popularized in Europe in the second edition of Behcet's Problèmes plaisance et délectables (Pleasant and enjoyable problems, 1624).
Did you mean: Their methods have the same answer as modern methods.
Did you mean: A modern expression of fractions known as vinnarasi seems to have originated in India in the work of Aryabhata, Brahmagupta, and Bhaskara.
Did you mean: Another fact worth noting is that the integers under multiplication is not a group—even if we exclude zero.
Did you mean: Computation with these fractions is equivalent to computing percentages.
Did you mean: The subtraction then proceeds in the hundreds place, where 6 is not less than 5, so the difference is written down in the results hundreds place.
Did you mean: Rather it increases the subtrahend hundreds digit by one.
Did you mean: The answer is 1, and is written down in the results hundreds place.
Did you mean: I have striven to compose this book in its entirety as understandable as I could, dividing it into fifteen chapters.
Did you mean: Since the base 1 exponential function (1 x) always equals 1, its inverse does not exist (which would be called the logarithm base 1 if it did exist).
Did you mean: The Mayans used a shell symbol to represent zero.
Did you mean: A facsimile globe showing America was made by Martin Waldseemuller in 1507.
Did you mean: Compared to the best fitting ellipsoid, and geoid model would change the characterization of important properties such as distance, conformality and equivalence.
Did you mean: However, it did not begin to dominate world maps until the 19th century, when the problem of position determination has been largely solved.
Did you mean: North is associated with the Himalayas and heaven while the south is associated with the underworld or land of the fathers (Pitru loka).
Did you mean: Geographical it is a Westward extension of the border between Virginia and North Carolina and part of the border between Kentucky and Tennessee.
Did you mean: The main techniques used in drawing are line drawing, hatching, cross hatching, random hatching, scribbling, stippling, and blending.
Did you mean: In the 16th century, Italian Mannerist architect, painter and theorist Sebastiano Serlio wrote Tutte L'Opere D'Architettura et Prospetiva (Complete Works on Architecture and Perspective).
Did you mean: In the qibla wall, usually at its center, is the mihrab, a niche or depression indicating the qibla wall.
Did you mean: Since these new architectural tendencies emerged, many theorists and architects have been working on these issues, developing theories and ideas such as Patrik Schumacher Parametricism.
Did you mean: Those in the Cathedral of Saint Mark, Venice (1071) especially attracted John Ruskin's fancy.
Did you mean: The Palaiologan period is well represented in a dozen former churches in Istanbul, notably St Saviour at Chora and St Mary Pammakaristos.
Did you mean: Sugar reconstructed portions of the old Romanesque church with the rib vault in order to remove walls and to make more space for windows.
Did you mean: Tiercerons – decorative vaulting ribs – seek first to be have been used in vaulting at Lincoln Cathedral, installed c.1200.
Did you mean: A variation of the spire was the flèche, a slender, spear-like spire, which was usually placed on the transept where it crosses the nave.
Did you mean: A similar arrangement was adopted in England, at Salisbury Cathedral, Lincoln Cathedral, and Ely Cathedral.
Did you mean: The sculptor Andrea Pisano made the celebrated bronze doors for Florence's Baptistery (1330–1336).
Did you mean: Some colleges, like Balliol College, Oxford, borrowed a military style from Gothic castles, with battlements and crenelated walls.
Showing translation for:  (use -no-auto to disable autocorrect)
Did you mean: The village buildings are grouped together within a defensive wall that includes corner towers and a gate.
Did you mean: At that time the U.S. feared that communism would spread to the Middle East, and it saw Nasser as a natural leader of an anti communist pro capitalist Arab League.
Did you mean: Al-Munifi stated that the Alexandrian Crusade in 1365 was divine punishment for a Sufi sheikh of the khanqah of Sa'id breaking off the nose.
Did you mean: The next reported European visitor to Lalibela was Miguel de Castanhal, who served as a soldier under Cristóvão da Gama and left Ethiopia in 1544.
Did you mean: Great Zimbabwe is a medieval city in the south-eastern hills of Zimbabwe near Lake Mutirikwi and the town of Masvingo.
Did you mean: Augustus Le Plongeon called it "Chac Mool" (later renamed "Chac Mool", which has been the term to describe all types of this statuary found in Mesoamerica).
Did you mean: The Mexican government excavated a tunnel from the base of the north staircase, up the earlier pyramids stairway to the hidden temple, and opened it to tourists.
Did you mean: The Temple of Xtoloc is a recently restored temple outside the Osorio Platform is.
Did you mean: Inside one of the chambers, near the ceiling, is a painted handprint.
Did you mean: The cleaning received the New York Landmarks Conservancy Lucy G. Moses Preservation Award for 1997.
Did you mean: For the rest, the aliens remain nameless.
Did you mean: 19th century romanticism emphasizes human agency and free will in meaning construction.
Did you mean: That is, since physics needs to talk about electrons to say why light bulbs behave as they do, the electrons must exist.
Did you mean: Physicalist monism asserts that the only existing substance is physical, in some sense of that term to be clarified by our best science.
Did you mean: The brain goes on from one moment of time to another; the brain that has identity through time.
Did you mean: This is the case for materialistic determinism.
Did you mean: Matranga, the principal governing body of these states, consisted of the King, Prime Minister, Commander in chief of army, Chief Priest of the King.
Did you mean: For example, the ideas of the Khawarij in the very early years of Islamic history on Khilafat and Ummah, or that of Shia Islam on the concept of Imamah are considered proofs of political thought.
Did you mean: Aristotelianism flourished as the Islamic Golden Age saw rise to a continuation of the peripatetic philosophers who implemented the ideas of Aristotle in the context of the Islamic world.
Did you mean: Other notable political philosophers of the time include Nizam al-Mulk, a Persian scholar and vizier of the Seljuk Empire who composed the Siyasatnama, or the "Book of Government" in English.
Did you mean: Along somewhat different lines, a number of other continental thinkers—still largely influenced by Marxism—put new emphasis on structuralism and on a "return to Hegel".
Did you mean: Notable for the theories that humans are social animals, and that the polis (Ancient Greek city state) exist to bring about the good life appropriate to such animals.
Did you mean: Plato: Wrote a lengthy dialogues The Republic in which he laid out his political philosophy: citizens should be divided into three categories.
Did you mean: It was first used by the German philosopher J.A. Eberhard as "vor sokratische Philosophy''' in the late 18th century.
Did you mean: After that is a code regarding whether the fragment is a testimonial, coded as "A", or "B" if is a direct quote from the philosopher.
Did you mean: In their effort to make sense of the cosmos they coined new terms and concepts such as rhythm, symmetry, analogy, reductionism, reductionism, mathematization of nature and others.
Did you mean: The Eleatics were also humanists (believed that only one thing exists and everything else is just a transformation of it).
Did you mean: The poem consists of three parts, the problem (i.s., preface), the Way of Truth and the Way of Opinion.
Showing translation for:  (use -no-auto to disable autocorrect)
Did you mean: Socrates taught that no one desires what is bad, and so if anyone does something that truly is bad, it must be unwilling or out of ignorance; consequently, all virtue is knowledge.
Did you mean: Later, under St. Abbo of Fleury (abbott 988–1004), head of the reformed abbey school, Fleury enjoyed a second golden age.
Did you mean: Further cultural subdivisions according to tool types, such as Oldowan or Mousterian or Levalloisian help archaeologists and other anthropologists in understanding major trends in the human past.
Did you mean: In Middle English, a "festival day" was a religious holiday.
Did you mean: Human behavioral ecology is the study of behavioral adaptations (foraging, reproduction, ontogeny) from the evolutionary and ecological perspectives (see behavioral ecology).
Did you mean: Other dimensions of racial groups include shared history, traditions, and language.
Did you mean: Moreover, the genomic data under determines whether one wishes to see subdivisions (i.e., splitters) or a continuum (i.e., lumpers).
Did you mean: 33 health services researchers from different geographic regions were interviewed in a 2008 study.
Did you mean: Calculations with numbers are done with arithmetic operations, the most familiar being addition, subtraction, multiplication, division, and exponentiation.
Did you mean: At the same time, the Chinese were indicating negative numbers by drawing a diagonal stroke through the right-most non-zero digit of the corresponding positive numbers numeral.
Did you mean: Fixed length integer approximation data types (or subsets) are denoted int or Integer in several programming languages (such as Algol 68, C, Java, Delphi, etc.).
Did you mean: Dirichlet also added to the general theory, as have numerous contributions to the applications of the subject.


"""

