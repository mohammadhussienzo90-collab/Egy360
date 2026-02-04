"""
Dramatic True Stories of Egypt - Captivating Historical Content
Warfare, Civilization, Mystery, Culture - Entertaining & Educational
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from blog.models import BlogPost
from django.contrib.auth.models import User

def get_author():
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.first()
    return author

DRAMATIC_STORIES = [
    {
        "title": "The Battle of Kadesh: When Egypt Faced Annihilation",
        "slug": "battle-of-kadesh-egypt-hittites-ramses",
        "meta_description": "1274 BC: Ramses II led 20,000 soldiers into the greatest chariot battle in history. What happened next changed the ancient world forever.",
        "excerpt": "The largest chariot battle ever fought. A pharaoh who walked into a trap. And a moment that nearly ended Egyptian civilization.",
        "image_url": "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80",
        "content": """
<h2>The Day Egypt Almost Fell</h2>

<p><em>1274 BC. The plains of Kadesh, modern-day Syria. Twenty thousand Egyptian soldiers marched toward what they believed would be an easy victory. They were walking into the greatest ambush in ancient history.</em></p>

<p>Ramses II was just 25 years old. Young. Ambitious. Convinced of his own immortality. He had inherited the most powerful empire on Earth, and he intended to expand it.</p>

<p>His target: the Hittite Empire. His enemy: King Muwatalli II, who had assembled the largest chariot army the world had ever seen.</p>

<h2>The Trap</h2>

<p>Two Bedouin nomads approached the Egyptian camp. They claimed to be deserters from the Hittite army. They had valuable intelligence: the Hittites were still far away, days of marching to the north.</p>

<p>Ramses believed them.</p>

<p>It was exactly what he wanted to hear. The young pharaoh pushed forward with only his personal division, leaving the rest of his army strung out for miles behind him.</p>

<p>The Bedouins were spies. The entire Hittite army—40,000 soldiers and 3,500 chariots—was hidden just across the river, waiting.</p>

<h2>The Ambush</h2>

<p>The Hittite chariots struck like a thunderbolt. They smashed through the Egyptian flank, scattering soldiers in every direction. Ramses' army dissolved into chaos.</p>

<p>Within minutes, the pharaoh found himself nearly alone, surrounded by enemy chariots, with his bodyguard fighting desperately to keep him alive.</p>

<p>According to Egyptian records, Ramses called out to the god Amun: <em>"I call to you, my father Amun. I am alone, with no one beside me. My soldiers have abandoned me. But I find that Amun is worth more than millions of soldiers."</em></p>

<p>What happened next became legend.</p>

<h2>The Counterattack</h2>

<p>Ramses personally led charge after charge into the Hittite lines. Whether divine intervention or military genius, he somehow held his ground long enough for reinforcements to arrive.</p>

<p>The battle raged for hours. Chariots crashed into chariots. The Orontes River ran red with blood. Thousands died on both sides.</p>

<p>By sunset, neither side had won. Both armies were shattered.</p>

<h2>The Aftermath</h2>

<p>The Battle of Kadesh ended in a draw—but that draw changed history.</p>

<p>Ramses returned to Egypt and covered every temple wall with depictions of his "great victory." The propaganda was so effective that for 3,000 years, historians believed he had actually won.</p>

<p>But the real outcome was more significant: sixteen years later, Egypt and the Hittites signed the world's first recorded peace treaty. A copy still hangs in the United Nations headquarters.</p>

<p>Two great empires, exhausted by war, chose peace instead. The treaty held for nearly a century.</p>

<h2>What You Can See Today</h2>

<p>Visit the Ramesseum in Luxor to see Ramses' own account of the battle carved into stone. The Abu Simbel temples feature massive depictions of the pharaoh charging into battle.</p>

<p>Walk where the greatest warrior-pharaoh walked. See the propaganda he created to immortalize himself. And remember that even the mightiest empires must eventually choose peace.</p>

<p><strong>The Battle of Kadesh teaches us that victory isn't always what we claim it to be—and sometimes, the greatest triumph is knowing when to stop fighting.</strong></p>
"""
    },
    {
        "title": "The Curse of the Pharaohs: Deaths That Defied Explanation",
        "slug": "curse-of-the-pharaohs-tutankhamun-deaths",
        "meta_description": "When Tutankhamun's tomb opened in 1922, the deaths began. Coincidence? Science? Or something darker? The true story of the pharaoh's curse.",
        "excerpt": "Lord Carnarvon died within weeks of entering the tomb. Then more deaths followed. Was it a curse, a fungus, or something we still don't understand?",
        "image_url": "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80",
        "content": """
<h2>The Warning Ignored</h2>

<p><em>November 26, 1922. The Valley of the Kings. Howard Carter held a candle to a small hole in an ancient doorway. Lord Carnarvon stood behind him, barely breathing.</em></p>

<p><em>"Can you see anything?" Carnarvon asked.</em></p>

<p><em>"Yes," Carter whispered. "Wonderful things."</em></p>

<p>They had just discovered the tomb of Tutankhamun—the most complete pharaonic burial ever found. Gold gleamed everywhere. Treasures untouched for 3,300 years.</p>

<p>But according to legend, they also unleashed something else.</p>

<h2>The First Death</h2>

<p>On April 5, 1923—less than five months after entering the tomb—Lord Carnarvon was dead.</p>

<p>The official cause: an infected mosquito bite that led to blood poisoning. But the circumstances were strange.</p>

<p>At the exact moment of his death in Cairo, the lights across the city went out. No explanation was ever found. Back in England, his dog reportedly howled and dropped dead at the same moment.</p>

<p>The newspapers went wild. "PHARAOH'S CURSE CLAIMS VICTIM," screamed the headlines.</p>

<h2>The Deaths That Followed</h2>

<p>Over the next decade, multiple people connected to the tomb's discovery died under unusual circumstances:</p>

<ul>
<li><strong>George Jay Gould</strong> - American financier who visited the tomb. Dead of fever within 24 hours.</li>
<li><strong>Prince Ali Kamel Fahmy Bey</strong> - Shot by his wife shortly after visiting.</li>
<li><strong>Sir Archibald Douglas Reid</strong> - Radiologist who x-rayed the mummy. Dead of mysterious illness.</li>
<li><strong>Hugh Evelyn-White</strong> - Archaeologist who helped excavate. Hanged himself, leaving a note: "I have succumbed to a curse."</li>
<li><strong>Sir Lee Stack</strong> - Governor-General of Sudan. Assassinated in Cairo.</li>
<li><strong>A.C. Mace</strong> - Carter's right-hand man. Died of arsenic poisoning.</li>
</ul>

<p>By some counts, over 20 people connected to the discovery died prematurely.</p>

<h2>The Rational Explanations</h2>

<p>Scientists have proposed several theories:</p>

<p><strong>Ancient Mold and Bacteria</strong>: Sealed for millennia, the tomb may have contained dangerous fungal spores. Aspergillus niger and other fungi were found in the tomb and can cause severe respiratory illness.</p>

<p><strong>Toxic Tomb Paint</strong>: Ancient Egyptians used arsenic and other poisonous substances in their paints and preservatives.</p>

<p><strong>Radiation</strong>: Some researchers suggest the tomb's granite contains low levels of radioactive materials.</p>

<p><strong>Statistical Coincidence</strong>: Howard Carter himself lived until 1939—17 years after opening the tomb. Many others involved lived long lives. We remember the dramatic deaths and forget the mundane survivals.</p>

<h2>The Mystery Endures</h2>

<p>Here's what we know for certain: multiple people who entered that tomb died in ways that seemed unusual. Whether curse, contamination, or coincidence, the pattern is striking.</p>

<p>The ancient Egyptians believed intensely in the power of words and magic. Tomb inscriptions often included warnings to those who would disturb the dead. One found in Tutankhamun's tomb reportedly read:</p>

<p><em>"Death shall come on swift wings to him who disturbs the peace of the King."</em></p>

<p>Did they know something we don't? Or were they simply protecting their treasures with the most powerful weapon available—fear?</p>

<h2>Visit the Tomb Today</h2>

<p>Tutankhamun's tomb is open to visitors in the Valley of the Kings. The golden treasures are now displayed at the Grand Egyptian Museum in Cairo.</p>

<p>Thousands of tourists enter the tomb every year. So far, the curse seems to have retired.</p>

<p>But as you descend those ancient steps, remember: you're walking where Lord Carnarvon walked. Into a darkness that has swallowed kings.</p>

<p><strong>Sweet dreams.</strong></p>
"""
    },
    {
        "title": "Cleopatra's Last Night: The Death That Ended an Empire",
        "slug": "cleopatra-death-last-pharaoh-true-story",
        "meta_description": "August 12, 30 BC: Cleopatra chose death over surrender. The true story of her final hours—and the snake that may never have existed.",
        "excerpt": "She ruled for 21 years. Seduced two Roman emperors. And on her last night alive, she made a choice that still haunts history.",
        "image_url": "https://images.unsplash.com/photo-1590073242678-70ee3fc28e8e?w=1200&q=80",
        "content": """
<h2>The Queen in the Mausoleum</h2>

<p><em>Alexandria, August 12, 30 BC. Cleopatra VII, the last pharaoh of Egypt, sat in the mausoleum she had built for herself. Roman soldiers surrounded the building. Her lover was dead. Her kingdom had fallen. Only one choice remained.</em></p>

<p>She was 39 years old. She had ruled Egypt for 21 years. She had seduced Julius Caesar and Marc Antony—the two most powerful men in the Roman world. She had borne children who were heirs to both Egyptian and Roman thrones.</p>

<p>And now it was over.</p>

<h2>The Fall</h2>

<p>Octavian's legions had crushed Marc Antony's forces at the Battle of Actium a year earlier. Now Octavian himself was in Alexandria, and Cleopatra was trapped.</p>

<p>Antony had already taken his own life—falling on his sword after receiving false news that Cleopatra was dead. With his final breaths, he was carried to her mausoleum, where he died in her arms.</p>

<p>Cleopatra tried to negotiate with Octavian. She was brilliant, charming, and still beautiful. She had seduced powerful men before.</p>

<p>But Octavian was different. He was cold. Calculating. He wanted only one thing: to parade the great Cleopatra through Rome in chains, the ultimate trophy of his conquest.</p>

<p>Cleopatra would not give him that satisfaction.</p>

<h2>The Final Act</h2>

<p>According to ancient accounts, Cleopatra dressed in her royal robes and lay on a golden couch. She had sent away most of her servants. Only two loyal handmaidens remained.</p>

<p>A basket of figs was brought to her. Hidden inside, supposedly, was an asp—an Egyptian cobra, the symbol of royalty.</p>

<p>When Octavian's soldiers broke into the mausoleum, they found Cleopatra dead. One handmaiden was dying; another was arranging the queen's crown.</p>

<p>"Was this right?" a soldier reportedly asked.</p>

<p>"It was entirely right," the handmaiden replied, "and fitting for a queen descended from so many kings." Then she collapsed and died.</p>

<h2>The Mystery</h2>

<p>But here's what most people don't know: the snake story might be legend.</p>

<p>No cobra was ever found in the mausoleum. Modern toxicologists point out that cobra venom causes violent convulsions—not the peaceful death the ancient sources describe.</p>

<p>Cleopatra was famous for her knowledge of poisons. She had studied them extensively, even testing them on condemned prisoners to find ones that killed quickly and painlessly.</p>

<p>Many historians now believe she used a carefully prepared poison—perhaps a combination of hemlock, wolfsbane, and opium—hidden in a hairpin or hollow container.</p>

<p>The snake was likely Roman propaganda, added later to make her death seem more exotic and barbaric—fitting their narrative of the decadent Eastern queen.</p>

<h2>The End of an Era</h2>

<p>With Cleopatra's death, three thousand years of pharaonic rule came to an end. Egypt became a Roman province. Her children were either killed or disappeared from history.</p>

<p>But Cleopatra achieved what she wanted: she died on her own terms, as a queen, with her royal dignity intact. Octavian got her kingdom, but not her humiliation.</p>

<p>Her tomb has never been found. Archaeologists have searched for centuries. Some believe it lies beneath Alexandria's harbor, sunk by ancient earthquakes. Others think it's still hidden, waiting to be discovered.</p>

<h2>Walk in Her Footsteps</h2>

<p>Visit Alexandria today and stand where Cleopatra once stood. The ancient lighthouse is gone, but the Citadel of Qaitbay was built from its stones. The Royal Library is rebuilt. The harbor where she welcomed Caesar still catches the Mediterranean sun.</p>

<p>Somewhere beneath those waters, perhaps, the last pharaoh waits.</p>

<p><strong>She was born a queen. She died a queen. And she became immortal.</strong></p>
"""
    },
    {
        "title": "The Lost Army of Cambyses: 50,000 Soldiers Swallowed by the Desert",
        "slug": "lost-army-cambyses-desert-mystery",
        "meta_description": "In 524 BC, a Persian army of 50,000 men marched into the Egyptian desert. They were never seen again. The mystery that has haunted historians for 2,500 years.",
        "excerpt": "They marched into a sandstorm and vanished. No survivors. No bodies. 50,000 soldiers erased from existence. What really happened?",
        "image_url": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=1200&q=80",
        "content": """
<h2>The Army That Vanished</h2>

<p><em>524 BC. The Western Desert of Egypt. Fifty thousand Persian soldiers marched toward the Siwa Oasis. They carried weapons, supplies, and the wrath of King Cambyses II. Somewhere in that endless sea of sand, they disappeared forever.</em></p>

<p>It remains one of history's greatest mysteries. An entire army—enough men to fill a modern football stadium—gone without a trace.</p>

<h2>The Madness of Cambyses</h2>

<p>Cambyses II had conquered Egypt two years earlier. He was the son of Cyrus the Great, ruler of the vast Persian Empire. But Egypt was proving difficult to control.</p>

<p>The priests of the Oracle at Siwa had prophesied against him. They called him illegitimate. They said the gods rejected him.</p>

<p>Cambyses responded as tyrants do: he sent an army to destroy the Oracle.</p>

<p>Fifty thousand men marched west from Thebes (modern Luxor). They were to cross 400 miles of desert, raze the Temple of Amun, and silence the priests forever.</p>

<p>They never arrived.</p>

<h2>What the Ancients Said</h2>

<p>The Greek historian Herodotus, writing 75 years later, recorded what he learned from Egyptian priests:</p>

<p><em>"A wind arose from the south, strong and deadly, bringing with it vast columns of whirling sand, which entirely covered up the troops and caused them wholly to disappear."</em></p>

<p>A sandstorm. The most powerful natural force in the Sahara. Walls of sand hundreds of feet high, moving at hurricane speeds, burying everything in their path.</p>

<p>It was plausible. Such storms still occur today.</p>

<p>But some historians suspected the story was Egyptian propaganda—a way to humiliate their Persian conquerors without admitting they couldn't find the army either.</p>

<h2>The Search</h2>

<p>For 2,500 years, explorers have searched for the Lost Army. The Western Desert is littered with the bones of those who tried.</p>

<p>In 1933, a Hungarian explorer reported finding Persian weapons and human bones, but he died before revealing the location.</p>

<p>In 2009, Italian archaeologists announced they had found the army: bronze weapons, silver jewelry, and massive bone fields in a remote area of the desert. They described finding skeletal remains scattered across a wide area, as if caught in the open by a sudden disaster.</p>

<p>But their claims remain controversial. Other experts dispute the evidence. The Egyptian government has not confirmed the find.</p>

<h2>The Theories</h2>

<p><strong>The Sandstorm</strong>: A massive khamsin could have buried the army alive. Such storms have killed travelers throughout history.</p>

<p><strong>Ambush</strong>: Some historians believe the army was attacked by desert tribes—perhaps the ancestors of the Siwa Berbers. They were led into a trap and massacred. The survivors were enslaved. The sandstorm story covered Egyptian involvement.</p>

<p><strong>Wrong Direction</strong>: The army may have become lost and wandered into the most desolate regions of the Sahara, dying of thirst before reaching any landmark.</p>

<p><strong>Desertion</strong>: Some theories suggest the army simply deserted, integrating into local populations or fleeing to other lands.</p>

<h2>The Desert Keeps Its Secrets</h2>

<p>Today, the Western Desert remains one of Earth's most forbidding landscapes. Temperatures reach 130°F (55°C). Water is scarce. Navigation is nearly impossible.</p>

<p>Somewhere out there, perhaps, lie the remains of 50,000 men—their bones, their weapons, their story waiting to be told.</p>

<p>Visit Siwa Oasis today and stand in the same Temple of Amun that the army was sent to destroy. It still stands. The Oracle was never silenced.</p>

<p>And somewhere in the desert, the Lost Army sleeps.</p>

<p><strong>The sand gives up nothing easily. But history is patient. One day, the desert may finally reveal what happened to the men who tried to silence the gods.</strong></p>
"""
    },
    {
        "title": "The Murder of Ramses III: A 3,000-Year-Old Crime Scene",
        "slug": "murder-ramses-iii-harem-conspiracy",
        "meta_description": "A pharaoh with his throat cut. A plot by his own wives. A trial that condemned princes to death. The true crime story of ancient Egypt.",
        "excerpt": "He survived battles against the Sea Peoples. He couldn't survive his own family. The assassination that rocked the ancient world.",
        "image_url": "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80",
        "content": """
<h2>The Wound That Hid for 3,000 Years</h2>

<p><em>1155 BC. The royal palace at Medinet Habu. Ramses III, one of Egypt's greatest warrior-kings, lay dead. The official story said he died peacefully. But someone in the palace knew the truth: the pharaoh had been murdered.</em></p>

<p>For three millennia, the secret stayed buried. Then, in 2012, CT scans revealed what ancient embalmers had carefully hidden: Ramses III's throat had been cut to the bone.</p>

<p>This is the true story of the Harem Conspiracy—ancient Egypt's most infamous assassination.</p>

<h2>The Warrior-King</h2>

<p>Ramses III was the last great pharaoh of the Egyptian Empire. He had defeated the Sea Peoples—mysterious invaders who destroyed every other Bronze Age civilization. He built the great temple at Medinet Habu. He expanded Egypt's power.</p>

<p>But he had enemies closer to home.</p>

<h2>The Queen's Plot</h2>

<p>Tiye was one of Ramses' many wives—but not his Great Royal Wife. Her son, Prince Pentawer, was not the crown prince. When Ramses died, another woman's son would become pharaoh.</p>

<p>Unless Ramses died sooner than expected.</p>

<p>Tiye recruited conspirators from within the palace: officials, military commanders, even servants. They planned to kill the king and place Pentawer on the throne.</p>

<p>Ancient documents describe how they used wax figurines and spells, attempting to weaken the pharaoh's guards through magic. Then they would strike.</p>

<h2>The Assassination</h2>

<p>The details of the attack itself are lost to history. But the CT scans tell a brutal story.</p>

<p>A sharp blade cut deep into Ramses' throat, severing the trachea and all major blood vessels. The wound was immediately fatal. Embalmers inserted a "Horus eye" amulet into the wound—a healing charm, perhaps placed in hope of restoring him in the afterlife.</p>

<p>They then wrapped the neck carefully, hiding the terrible evidence.</p>

<h2>The Trial</h2>

<p>The assassination was discovered. Whether the plot succeeded temporarily or was stopped immediately remains unclear.</p>

<p>What we do know is that a massive trial followed. The "Judicial Papyrus of Turin" documents the proceedings.</p>

<p>Forty people were accused. The charges: conspiracy, sedition, murder.</p>

<p>The verdicts were brutal:</p>

<ul>
<li>Queen Tiye: verdict unknown (likely executed)</li>
<li>Prince Pentawer: condemned to suicide (he was allowed to take his own life rather than be executed as a commoner)</li>
<li>Court officials: noses and ears cut off, then executed</li>
<li>Military commanders: forced to commit suicide</li>
<li>Servants: executed</li>
</ul>

<h2>The Screaming Mummy</h2>

<p>In 2012, DNA analysis identified a mysterious mummy known as "Unknown Man E" as Prince Pentawer himself. The mummy is famous for its horrific expression—mouth wide open in what appears to be a scream.</p>

<p>The body was wrapped in sheep skin (ritually unclean), denied proper mummification, and buried without organs or proper rites. It was the ultimate disgrace for an Egyptian prince.</p>

<p>Some believe his expression captures his final moments—forced to drink poison while conscious. Others suggest the jaw simply dropped after death.</p>

<p>Either way, his punishment continued beyond the grave.</p>

<h2>Visit the Crime Scene</h2>

<p>Medinet Habu, Ramses III's mortuary temple, still stands near Luxor. Its walls are covered with scenes of his military victories—ironic, given how he actually died.</p>

<p>The mummy of Ramses III can be seen at the National Museum of Egyptian Civilization in Cairo, his fatal wound hidden beneath ancient bandages.</p>

<p>Prince Pentawer's screaming mummy is in storage—too disturbing for public display.</p>

<p>Walk through the palace where the conspiracy was hatched. Stand in the temple where a king was mourned. And remember that even pharaohs couldn't escape the oldest motive of all.</p>

<p><strong>Power. Ambition. Betrayal. Some things never change.</strong></p>
"""
    },
    {
        "title": "The Night They Moved Abu Simbel: Engineering the Impossible",
        "slug": "moving-abu-simbel-engineering-marvel",
        "meta_description": "In 1968, engineers cut two ancient temples into pieces and moved them 200 feet up a cliff. The incredible true story of saving Abu Simbel.",
        "excerpt": "The Nile was rising. Ramses II's greatest temple would be underwater in years. A Swedish engineer had a crazy idea—cut it apart and rebuild it higher.",
        "image_url": "https://images.unsplash.com/photo-1608649672510-2b4aeb84f2f3?w=1200&q=80",
        "content": """
<h2>The Temple the World Refused to Lose</h2>

<p><em>1959. The Egyptian government announced plans to build the Aswan High Dam. It would bring electricity and irrigation to millions. It would also drown one of humanity's greatest treasures: the temples of Abu Simbel.</em></p>

<p>For 3,200 years, four colossal statues of Ramses II had gazed across the Nile. Each was 66 feet tall. Each weighed over 1,000 tons. They were carved directly into a sandstone cliff.</p>

<p>In just years, they would be at the bottom of a lake.</p>

<h2>The Impossible Problem</h2>

<p>The new dam would create Lake Nasser—one of the world's largest artificial lakes. Water would rise over 200 feet. Abu Simbel would be completely submerged.</p>

<p>Losing Abu Simbel was unthinkable. But how do you move a mountain?</p>

<p>The world responded. UNESCO launched the largest archaeological rescue operation in history. Fifty countries contributed funding and expertise.</p>

<p>Several plans were proposed:</p>

<ul>
<li>Build a glass dome around the temples and let tourists view them underwater</li>
<li>Float the entire cliff on pontoons</li>
<li>Let the temples flood and build replicas elsewhere</li>
</ul>

<p>Then a Swedish engineering firm proposed something audacious: cut the temples into pieces, move them block by block, and reassemble them 200 feet higher.</p>

<h2>The Cutting Begins</h2>

<p>In 1964, workers began slicing through 3,200 years of history.</p>

<p>The temples were cut into 1,036 blocks, each weighing between 20 and 30 tons. Every cut had to be precise—too deep and the sandstone would crumble; too shallow and the blocks wouldn't separate.</p>

<p>Workers used hand saws for the most delicate areas. The faces of the colossi were cut from behind, leaving the features intact.</p>

<p>Each block was carefully numbered, photographed, and catalogued. Engineers created detailed maps showing exactly where each piece belonged.</p>

<p>It took four years. It cost $40 million (over $300 million today). But piece by piece, the temples were disassembled.</p>

<h2>The Reconstruction</h2>

<p>An artificial mountain was built 200 feet above and 690 feet back from the original location. The blocks were lifted by crane and reassembled like the world's heaviest jigsaw puzzle.</p>

<p>The precision was extraordinary. When the temple was complete, the alignment matched exactly: twice a year, on February 22 and October 22, sunlight still penetrates the inner sanctuary to illuminate the statues of the gods—just as Ramses intended.</p>

<p>The dates mark Ramses' birthday and coronation. After 3,200 years and a 200-foot move, the engineering still works.</p>

<p>Concrete domes were built behind the reconstructed cliff faces to support the structure. Today, visitors walk through the temples unaware they're inside a modern shell.</p>

<h2>The Second Temple</h2>

<p>Beside Abu Simbel stands the smaller temple of Nefertari—Ramses' beloved queen. It too was cut into blocks and moved.</p>

<p>Its inscription remains one of ancient Egypt's most romantic: "She for whom the sun shines."</p>

<h2>What It Means</h2>

<p>The rescue of Abu Simbel proved something important: humanity can preserve its heritage when it chooses to.</p>

<p>The project inspired the 1972 World Heritage Convention, which protects sites around the globe. Abu Simbel showed that international cooperation could achieve the impossible.</p>

<p>Visit today and you're looking at both ancient Egypt and modern engineering. Ramses built for eternity. We proved him right.</p>

<h2>Visiting Abu Simbel</h2>

<p>The temples are 280 km south of Aswan. Most visitors fly in for the day or take a convoy across the desert.</p>

<p>Arrive for sunrise. Watch the light creep across the lake. See the colossi glow gold and pink.</p>

<p>And remember: what you're seeing shouldn't exist. A lake should be here. The pharaoh should be underwater.</p>

<p>Instead, he watches over the Nile as he has for 3,200 years—thanks to human beings who refused to let history drown.</p>

<p><strong>Ramses built a temple to last forever. We made sure it would.</strong></p>
"""
    },
    {
        "title": "The Exodus Mystery: Did Moses Really Part the Red Sea?",
        "slug": "exodus-moses-red-sea-historical-evidence",
        "meta_description": "One of history's most famous stories—but did it happen? The archaeological evidence, scientific theories, and enduring mystery of the Exodus.",
        "excerpt": "Millions believe Moses led the Israelites out of Egypt. But what does science say? The search for evidence of the greatest escape in history.",
        "image_url": "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80",
        "content": """
<h2>The Story That Shaped History</h2>

<p><em>"And Moses stretched out his hand over the sea; and the LORD caused the sea to go back by a strong east wind all that night, and made the sea dry land, and the waters were divided."</em> — Exodus 14:21</p>

<p>It's one of the most famous scenes in religious history: Moses raising his staff, waters parting, hundreds of thousands of Israelites walking to freedom while Pharaoh's army drowns behind them.</p>

<p>But did it really happen? And if so, how?</p>

<h2>What History Says</h2>

<p>Here's the uncomfortable truth: there is no direct archaeological evidence of the Exodus.</p>

<p>Egyptian records mention no mass departure of slaves. No graves of 600,000 men (plus women and children) have been found in the Sinai. No Egyptian artifacts appear in early Israelite settlements.</p>

<p>But absence of evidence isn't evidence of absence. Egyptians routinely erased embarrassing events from their records. The Sinai is vast and mostly unexcavated. And some intriguing clues do exist.</p>

<h2>The Clues</h2>

<p><strong>The Merneptah Stele (1208 BC)</strong>: The earliest known reference to "Israel" outside the Bible. Pharaoh Merneptah boasts of destroying Israel in Canaan. For him to destroy them, they had to exist.</p>

<p><strong>Semitic Slaves in Egypt</strong>: Papyri confirm that Semitic-speaking slaves worked on Egyptian construction projects during the relevant period. They were called "Apiru"—which some connect to "Hebrew."</p>

<p><strong>The Hyksos Expulsion</strong>: Around 1550 BC, Egypt expelled the Hyksos—Semitic rulers who had controlled northern Egypt for over a century. Some scholars suggest this event morphed into the Exodus story over generations.</p>

<p><strong>Volcanic Evidence</strong>: Some researchers connect the plagues to the eruption of Thera (Santorini) around 1600 BC—which could have caused darkness, blood-red waters, and other phenomena.</p>

<h2>The Red Sea: Science or Miracle?</h2>

<p>First, a translation issue: the Hebrew says "Yam Suph," which means "Sea of Reeds"—not Red Sea. This likely refers to shallow lakes in the Nile Delta, not the deep Red Sea.</p>

<p>And here's where it gets interesting: modern science has shown that wind can push shallow water aside.</p>

<p>In 2010, researchers at the National Center for Atmospheric Research simulated a strong east wind—exactly what the Bible describes—blowing over a reconstructed ancient lagoon. The result: a land bridge appeared for four hours before the water rushed back.</p>

<p>Natural phenomenon? Divine timing? Both?</p>

<h2>The Pharaoh Question</h2>

<p>The Bible never names the pharaoh of the Exodus. Candidates include:</p>

<ul>
<li><strong>Ramses II</strong>: The traditional choice, based on the construction of the city called Ramses</li>
<li><strong>Thutmose III</strong>: Dates match some archaeological evidence</li>
<li><strong>Ahmose I</strong>: His expulsion of the Hyksos might be the origin story</li>
</ul>

<p>None of their mummies show signs of drowning. But if the pharaoh sent his army but stayed behind, there would be no body to find in the sea.</p>

<h2>What It Means</h2>

<p>Whether the Exodus happened exactly as described, was a smaller event that grew in the telling, or was a composite of multiple historical memories, its impact is undeniable.</p>

<p>The Exodus story shaped Judaism, Christianity, and Islam. It inspired abolitionists and civil rights activists. It gave hope to the oppressed throughout history.</p>

<p>Sometimes the truth of a story lies not in its archaeological evidence but in its power to move human hearts.</p>

<h2>Walk the Path</h2>

<p>Visit Egypt and trace the possible routes: the Nile Delta, where slaves may have labored; the Sinai Peninsula, where they may have wandered; Mount Sinai (Jebel Musa), where Moses may have received the commandments.</p>

<p>Stand at the Red Sea coast. Watch the wind blow across the water.</p>

<p>And wonder.</p>

<p><strong>Some mysteries aren't meant to be solved. They're meant to be lived.</strong></p>
"""
    },
    {
        "title": "The Woman Who Ruled as King: Hatshepsut's Secret Power",
        "slug": "hatshepsut-female-king-erased-history",
        "meta_description": "She declared herself pharaoh, wore a false beard, and ruled Egypt for 22 years. Then her stepson tried to erase her from history. The remarkable story of Hatshepsut.",
        "excerpt": "She dressed as a man. She called herself king. She built monuments that still stand. And then someone tried to make the world forget she ever existed.",
        "image_url": "https://images.unsplash.com/photo-1609949279531-cf48d64bed89?w=1200&q=80",
        "content": """
<h2>The Woman Who Became King</h2>

<p><em>1479 BC. A woman sat on the throne of Egypt. Not as queen. Not as regent. As pharaoh—god-king of the most powerful nation on Earth. She wore the false beard. She used the male pronouns. Her name was Hatshepsut, and she would rule for 22 years.</em></p>

<p>It was unprecedented. It was audacious. And it almost disappeared from history forever.</p>

<h2>The Path to Power</h2>

<p>Hatshepsut was born a princess, daughter of Pharaoh Thutmose I. She married her half-brother, Thutmose II (as was common for Egyptian royalty). When he died young, the throne passed to his son by another wife—Thutmose III, still a child.</p>

<p>Hatshepsut became regent, ruling on behalf of her young stepson.</p>

<p>Then, around year seven of the regency, she did something extraordinary: she declared herself pharaoh.</p>

<p>Not queen. Not regent. Pharaoh. King of Upper and Lower Egypt.</p>

<h2>Becoming Male</h2>

<p>Egyptian ideology required the pharaoh to be male—the earthly embodiment of Horus, the living god. Hatshepsut solved this problem with a combination of propaganda and audacity.</p>

<p>She ordered statues showing herself with a male body. She wore the traditional pharaonic false beard. Official inscriptions referred to her with male pronouns.</p>

<p>But she didn't try to pretend she was actually male. Some statues show her with breasts. Inscriptions called her "Daughter of Re" even while using male titles.</p>

<p>She was inventing a new kind of rule—and she knew exactly what she was doing.</p>

<h2>The Great Builder</h2>

<p>Hatshepsut's reign was marked not by war but by construction. Her mortuary temple at Deir el-Bahari is one of ancient Egypt's architectural masterpieces—elegant columns, terraced gardens, and walls covered with scenes of her accomplishments.</p>

<p>She sent a famous expedition to the land of Punt (probably modern Somalia or Eritrea), bringing back exotic goods, incense trees, and live baboons. The voyage is depicted in detail on her temple walls.</p>

<p>She erected two of the largest obelisks ever built at Karnak. One still stands today.</p>

<p>Under her rule, Egypt prospered. Trade flourished. The economy grew. There is no evidence of rebellions or foreign invasions.</p>

<h2>The Erasure</h2>

<p>Hatshepsut died around 1458 BC. Thutmose III—now an adult—finally became sole ruler.</p>

<p>Then, about 20 years later, something strange happened: workers began systematically destroying Hatshepsut's monuments. Her statues were smashed. Her images were chiseled off temple walls. Her name was removed from king lists.</p>

<p>Why? Scholars have debated for generations.</p>

<p>Early theories suggested Thutmose III hated his stepmother for stealing his throne. But the delay makes this unlikely—why wait 20 years for revenge?</p>

<p>Modern scholars believe it was about succession. Thutmose III was arranging for his own son to succeed him. Having a female pharaoh in the official history complicated matters. Better to erase the anomaly.</p>

<p>It almost worked. For three thousand years, Hatshepsut was largely forgotten.</p>

<h2>The Rediscovery</h2>

<p>In the 19th century, archaeologists began piecing together the clues. A temple without a pharaoh. Statues with chiseled-out faces. Male pronouns that didn't quite fit.</p>

<p>Slowly, Hatshepsut emerged from oblivion. Her temple was restored. Her mummy was identified in 2007. Her story was finally told.</p>

<h2>Visit Her Legacy</h2>

<p>Her mortuary temple at Deir el-Bahari, across the Nile from Luxor, is stunning. Arrive early to beat the heat and crowds. Walk up the terraced ramps. Imagine a woman who refused to be limited by what was "possible."</p>

<p>At Karnak, her obelisks still pierce the sky. One is the tallest surviving ancient Egyptian obelisk.</p>

<p>Her mummy rests in the Egyptian Museum, finally honored after millennia of erasure.</p>

<p>They tried to make the world forget her. They failed.</p>

<p><strong>Some legacies cannot be erased. Some women refuse to disappear.</strong></p>
"""
    },
    {
        "title": "The Bent Pyramid: When Ancient Engineers Made a Mistake",
        "slug": "bent-pyramid-dahshur-engineering-failure",
        "meta_description": "Halfway up, the angle changes. Something went wrong. The Bent Pyramid tells the story of ancient Egypt's most visible engineering mistake—and what they learned from it.",
        "excerpt": "It's the strangest pyramid in Egypt. Halfway up, the angle suddenly changes. What happened? The fascinating story of learning from failure.",
        "image_url": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80",
        "content": """
<h2>The Pyramid That Changed Its Mind</h2>

<p><em>Dahshur, 25 miles south of Cairo. A pyramid rises from the desert—but something is wrong. Halfway up, the angle shifts dramatically, giving it a bent, almost broken appearance. This is the Bent Pyramid, and it tells one of archaeology's most fascinating stories: what happens when ambition meets reality.</em></p>

<h2>The Original Plan</h2>

<p>Pharaoh Sneferu wanted the biggest, steepest pyramid ever built. Around 2600 BC, his architects began construction at an ambitious 54-degree angle—steeper than any pyramid before.</p>

<p>For the first 165 feet, everything went according to plan. The limestone blocks rose toward the sky at their dramatic angle.</p>

<p>Then disaster struck.</p>

<h2>Something Went Wrong</h2>

<p>Cracks appeared. The internal chambers began to deform. The massive weight of the stone was too much for the steep angle.</p>

<p>Some historians believe an actual collapse occurred during construction. Others think the engineers simply realized they were heading for catastrophe.</p>

<p>Either way, they had a choice: abandon the pyramid or find a solution.</p>

<p>They chose to adapt.</p>

<h2>The Change</h2>

<p>At 165 feet, the angle suddenly changes from 54 degrees to 43 degrees. The pyramid continues upward, but at a much gentler slope.</p>

<p>The result is the distinctive "bent" shape—a permanent monument to a problem solved in real-time.</p>

<p>The original design would have created a 420-foot pyramid. The compromise reached 344 feet. Still massive, but humbler.</p>

<h2>The Real Innovation</h2>

<p>Here's what makes this story remarkable: the Bent Pyramid isn't a failure. It's a learning experience frozen in stone.</p>

<p>Look inside and you'll see the real innovations. For the first time, architects used cedar beams to reinforce the internal chambers. They adjusted the corbelled ceiling design. They developed new techniques for distributing weight.</p>

<p>These solutions would be refined in every pyramid that followed.</p>

<h2>The Second Attempt</h2>

<p>Sneferu didn't give up. Just a mile north, he built another pyramid—the Red Pyramid. This time, he used the gentler 43-degree angle from the start.</p>

<p>It worked. The Red Pyramid was Egypt's first true smooth-sided pyramid—the direct ancestor of the Great Pyramid at Giza.</p>

<p>Sneferu's son, Khufu, would apply everything learned at Dahshur to build the Great Pyramid. The errors at the Bent Pyramid directly enabled the wonder at Giza.</p>

<h2>Failure as Progress</h2>

<p>The Bent Pyramid teaches a powerful lesson: innovation requires failure.</p>

<p>Sneferu's architects could have hidden their mistake. They could have demolished the pyramid and started over. Instead, they left it standing—a permanent record of the learning process.</p>

<p>Today, we can see exactly what went wrong and how they fixed it. It's an engineering textbook written in stone.</p>

<h2>Visiting Dahshur</h2>

<p>Dahshur is less crowded than Giza and arguably more interesting. You can:</p>

<ul>
<li>Walk around the Bent Pyramid's exterior (reopened in 2019 for the first time in 50 years)</li>
<li>Enter the Red Pyramid—one of the few pyramids you can explore inside</li>
<li>Stand in the burial chamber deep within the stone</li>
</ul>

<p>It's a 45-minute drive from Cairo. Most visitors combine it with nearby Saqqara and Memphis.</p>

<p>Stand at the base of the Bent Pyramid. Look up at that dramatic angle change. And remember: you're looking at the moment ancient Egypt learned to build wonders.</p>

<p><strong>Every masterpiece has a story of failure behind it. The Bent Pyramid is honest enough to show you its scars.</strong></p>
"""
    },
    {
        "title": "The Rosetta Stone: How a Broken Slab Changed Everything",
        "slug": "rosetta-stone-deciphering-hieroglyphics",
        "meta_description": "For 1,400 years, no one could read hieroglyphics. Then a French soldier found a broken stone in the Nile Delta. The race to unlock ancient Egypt's secrets.",
        "excerpt": "Hieroglyphics were a dead language for fourteen centuries. Then came Napoleon, a lucky discovery, and a rivalry that would crack the code.",
        "image_url": "https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200&q=80",
        "content": """
<h2>The Language That Died</h2>

<p><em>For 3,000 years, the ancient Egyptians wrote in hieroglyphics—sacred symbols carved into temple walls, painted on coffins, inscribed on papyrus. Then, around 400 AD, the last person who could read them died. The language fell silent for 1,400 years.</em></p>

<p>Every pyramid, every temple, every tomb was covered in messages no one could understand. The ancient Egyptians were speaking to us across millennia—and we couldn't hear a word.</p>

<h2>The Discovery</h2>

<p>July 1799. Napoleon's army was rebuilding a fort near the town of Rosetta in the Nile Delta. A soldier named Pierre-François Bouchard noticed something in the rubble: a dark stone slab covered in inscriptions.</p>

<p>The stone contained the same text written in three scripts: hieroglyphics at the top, Demotic (everyday Egyptian script) in the middle, and ancient Greek at the bottom.</p>

<p>The officers recognized immediately what this meant: if they could read the Greek, they might be able to decode the hieroglyphics.</p>

<p>For the first time in 1,400 years, there was a key to the ancient world.</p>

<h2>The Race</h2>

<p>When the British defeated Napoleon in Egypt, they seized the Rosetta Stone as a prize of war. It went to the British Museum, where it remains today.</p>

<p>But copies had already been made. Scholars across Europe began the race to crack the code.</p>

<p>Two men led the competition:</p>

<p><strong>Thomas Young</strong>, English polymath, made early breakthroughs. He realized that cartouches (oval borders) contained royal names. He identified the name "Ptolemy" in hieroglyphics.</p>

<p><strong>Jean-François Champollion</strong>, French linguist, took it further. He had studied Coptic—the language descended from ancient Egyptian—since childhood. He understood what Young didn't: hieroglyphics weren't just symbols, they were a complex writing system with both phonetic and ideographic elements.</p>

<h2>The Breakthrough</h2>

<p>September 14, 1822. Champollion received copies of inscriptions from Abu Simbel. He studied them, comparing to his Rosetta Stone work.</p>

<p>Suddenly, it clicked.</p>

<p>He ran to his brother's office, threw the papers on the desk, and shouted "Je tiens l'affaire!" ("I've got it!") Then he collapsed unconscious and slept for five days, exhausted by the mental effort.</p>

<p>When he woke, he had unlocked ancient Egypt.</p>

<h2>What He Discovered</h2>

<p>Champollion realized hieroglyphics worked multiple ways simultaneously:</p>

<ul>
<li>Some symbols represented sounds (like an alphabet)</li>
<li>Some represented entire words (like Chinese characters)</li>
<li>Some were "determinatives" that clarified meaning without being pronounced</li>
</ul>

<p>It was fiendishly complex—and beautiful. The ancient Egyptians had created one of history's most sophisticated writing systems.</p>

<p>With the code cracked, suddenly the pyramids spoke. Temple inscriptions revealed their meanings. The Book of the Dead could be read. King lists identified pharaohs. Medical texts, love poems, legal contracts—3,000 years of human experience opened up.</p>

<h2>The Stone Today</h2>

<p>The Rosetta Stone sits in the British Museum, where it has been since 1802. It remains one of the most visited objects in any museum.</p>

<p>It's smaller than most people expect—about 4 feet tall, 2.5 feet wide. The top is broken off (probably containing more hieroglyphic text). The surface is covered in precise, elegant inscriptions.</p>

<p>The text itself is mundane: a decree from priests praising King Ptolemy V. The content is forgettable. The implications changed the world.</p>

<h2>Egypt Wants It Back</h2>

<p>The Egyptian government has repeatedly requested the stone's return. The British Museum has refused. The debate continues.</p>

<p>For now, visitors can see the stone in London or view replicas in the Egyptian Museum in Cairo.</p>

<h2>The Living Legacy</h2>

<p>Thanks to Champollion, today we can read ancient Egyptian as fluently as Latin or Greek. We know the names of pharaohs, the prayers of priests, the complaints of workers, the dreams of scribes.</p>

<p>One broken stone. Two scholars. Fourteen centuries of silence, finally broken.</p>

<p><strong>The ancient Egyptians believed words had power—that speaking a name gave it life. They were right. Their words live again.</strong></p>
"""
    },
    {
        "title": "The Sea Peoples: The Mysterious Invaders Who Almost Destroyed Civilization",
        "slug": "sea-peoples-bronze-age-collapse-mystery",
        "meta_description": "Around 1200 BC, mysterious warriors from the sea destroyed every major civilization except Egypt. Who were they? Where did they come from? The greatest mystery of the ancient world.",
        "excerpt": "They came from the sea and burned everything. The Hittites fell. Mycenae fell. Troy fell. Only Egypt survived to tell the tale. Who were the Sea Peoples?",
        "image_url": "https://images.unsplash.com/photo-1569949381669-ecf31ae8e613?w=1200&q=80",
        "content": """
<h2>The End of the World</h2>

<p><em>Around 1200 BC, civilization collapsed. The Hittite Empire—which had ruled much of the Middle East for centuries—vanished. Mycenaean Greece fell into a dark age. Troy burned. Cyprus was devastated. City after city along the Mediterranean coast was destroyed and never rebuilt.</em></p>

<p><em>Only Egypt survived. And Egyptian records tell of a terrifying enemy: warriors who "came from the sea."</em></p>

<p>They are called the Sea Peoples. After 3,200 years, we still don't know exactly who they were.</p>

<h2>What the Egyptians Recorded</h2>

<p>The walls of Medinet Habu, Ramses III's mortuary temple near Luxor, contain the most detailed account of the Sea Peoples.</p>

<p>The inscriptions describe a massive invasion around 1178 BC:</p>

<p><em>"The foreign countries made a conspiracy in their islands. All at once the lands were removed and scattered in the fray. No land could stand before their arms. They were coming forward toward Egypt while the flame was prepared before them."</em></p>

<p>The carvings show distinctive warriors with horned helmets, round shields, and long swords. They fought from ships with raised bows. They brought their families in ox-carts, suggesting they came to settle, not just raid.</p>

<h2>Who Were They?</h2>

<p>Egyptian records name specific groups: the Peleset, Tjeker, Shekelesh, Denyen, and Weshesh. But these names raise more questions than answers.</p>

<p>Theories abound:</p>

<p><strong>The Peleset</strong> may be the Philistines, who later settled in what is now Gaza. DNA evidence supports a connection to the Aegean.</p>

<p><strong>The Sherden</strong> may have come from Sardinia—or may have later settled there. They wore distinctive horned helmets.</p>

<p><strong>The Denyen</strong> might be connected to the Greek Danaans mentioned in Homer.</p>

<p><strong>The Lukka</strong> may have come from Lycia in modern Turkey.</p>

<p>But were they a unified force? A loose confederation? Multiple unrelated groups that Egyptian scribes lumped together? No one knows for certain.</p>

<h2>The Battle of the Delta</h2>

<p>Ramses III met the Sea Peoples in the Nile Delta. The battle was massive—both on land and at sea.</p>

<p>Egyptian archers stationed on shore poured arrows into enemy ships. The distinctive Egyptian vessels, with their high bows and sterns, rammed the Sea Peoples' boats. Egyptian soldiers boarded and fought hand-to-hand.</p>

<p>The carvings at Medinet Habu show the chaos: ships capsizing, warriors drowning, bodies floating in the water.</p>

<p>Egypt won. The Sea Peoples were defeated.</p>

<p>But every other major civilization they attacked was destroyed.</p>

<h2>The Great Mystery</h2>

<p>Why did the Bronze Age collapse so completely? The Sea Peoples are part of the answer, but probably not the whole explanation.</p>

<p>Modern theories suggest a "systems collapse":</p>

<ul>
<li><strong>Climate change</strong>: Evidence suggests severe droughts hit the eastern Mediterranean around 1200 BC, destroying harvests.</li>
<li><strong>Earthquakes</strong>: A series of major earthquakes struck multiple cities within decades of each other.</li>
<li><strong>Economic disruption</strong>: The interconnected Bronze Age trade network depended on tin from distant sources. Disruption anywhere affected everywhere.</li>
<li><strong>Internal rebellions</strong>: Several cities show evidence of destruction from within, not outside attack.</li>
</ul>

<p>The Sea Peoples may have been refugees themselves—displaced by the same catastrophes they inflicted on others, driven to attack because their own homes had been destroyed.</p>

<h2>The Survivors</h2>

<p>Egypt survived but was weakened. Within a century, the great empire would fracture. The New Kingdom would end.</p>

<p>Some Sea Peoples settled along the coast. The Philistines built cities in Gaza. Their culture blended Aegean and local traditions.</p>

<p>The Bronze Age was over. The Iron Age—with new technologies, new powers, and new forms of writing—would eventually rise from the ashes.</p>

<h2>See the Evidence</h2>

<p>Visit Medinet Habu in Luxor to see the Sea Peoples depicted in stone. The relief carvings are remarkably detailed—you can see their helmets, weapons, and ships.</p>

<p>At the Egyptian Museum in Cairo (and soon the Grand Egyptian Museum), you can see artifacts from Ramses III's reign, including weapons captured from the invaders.</p>

<p>Stand before those walls and imagine the terror: strange ships appearing on the horizon, cities burning along the coast, the world as they knew it ending.</p>

<p>Egypt faced the apocalypse—and survived to tell the story.</p>

<p><strong>Some mysteries may never be solved. The Sea Peoples remain ghosts of history—known only by the destruction they left behind and the civilization strong enough to stop them.</strong></p>
"""
    }
]

def seed_dramatic_stories():
    """Seed dramatic historical stories"""
    print("\nSeeding Dramatic True Stories of Egypt...\n")
    print("Stories of warfare, mystery, civilization, and culture\n")

    author = get_author()
    created = 0

    for story in DRAMATIC_STORIES:
        post, was_created = BlogPost.objects.get_or_create(
            slug=story['slug'],
            defaults={
                'title': story['title'],
                'content': story['content'],
                'excerpt': story['excerpt'],
                'meta_description': story['meta_description'][:160],
                'image_url': story['image_url'],
                'status': 'published',
                'author': author
            }
        )

        if was_created:
            created += 1
            print(f"CREATED: {story['title'][:55]}...")
        else:
            print(f"EXISTS:  {story['title'][:55]}...")

    total = BlogPost.objects.count()
    print(f"\nCreated: {created} | Total articles: {total}")
    print("\nDramatic stories ready to captivate readers!")

if __name__ == '__main__':
    seed_dramatic_stories()
