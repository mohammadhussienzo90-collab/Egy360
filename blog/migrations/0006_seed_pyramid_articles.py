# Generated migration to seed Great Pyramid blog articles
from django.db import migrations
from django.utils import timezone


def create_pyramid_articles(apps, schema_editor):
    """Create the 9 Great Pyramid blog articles."""
    BlogPost = apps.get_model('blog', 'BlogPost')
    BlogCategory = apps.get_model('blog', 'BlogCategory')
    User = apps.get_model('auth', 'User')

    # Get or create category
    category, _ = BlogCategory.objects.get_or_create(
        slug='ancient-egypt',
        defaults={'name': 'Ancient Egypt', 'description': 'Explore the wonders of Ancient Egypt - pyramids, temples, pharaohs, and mysteries.'}
    )

    # Get admin user
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.first()
    if not author:
        return  # No users, skip

    now = timezone.now()

    articles = [
        {
            'title': 'The Great Pyramid of Giza: 4,500 Years of Mystery and Marvel',
            'slug': 'great-pyramid-giza-introduction',
            'excerpt': 'Discover the mind-blowing facts about the Great Pyramid of Giza - the only surviving Wonder of the Ancient World. From its impossible precision to its enduring mysteries.',
            'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',
            'meta_description': 'Explore the Great Pyramid of Giza - 4,500 years old, 2.3 million blocks, and still full of mysteries. The complete introduction guide.',
            'meta_keywords': 'great pyramid, giza, khufu, cheops, ancient egypt, seven wonders, pyramids',
            'tags': 'pyramids, giza, khufu, ancient egypt, world wonders',
            'is_featured': True,
            'content': '''## The Wonder That Defies Time

Standing on the Giza Plateau, just outside modern Cairo, the Great Pyramid has watched over Egypt for more than four and a half millennia. It is the only surviving Wonder of the Ancient World, and for good reason - nothing else comes close to its scale, precision, and enduring mystery.

## Mind-Blowing Numbers

Let's start with the statistics that will reshape how you think about ancient civilizations:

### Height and Scale
- **Original height:** 146.6 meters (481 feet) - the equivalent of a 48-story building
- **Current height:** 138.8 meters (the top has eroded over time)
- **Record holder:** The tallest structure on Earth for 3,800 years, until Lincoln Cathedral was built in 1311 CE

### The Building Blocks
- **Total blocks:** Approximately 2.3 million stone blocks
- **Weight range:** Each block weighs between 2.5 and 80 tons
- **Total weight:** Estimated 6 million tons
- **Volume:** 2.5 million cubic meters of stone

### Impossible Precision
- **Base length:** 230.4 meters per side
- **Accuracy:** The four sides differ by only 4.4 centimeters - that's 99.98% perfect symmetry
- **Alignment:** Oriented to true north with an error of just 3/60th of a degree
- **Level base:** Varies by only 2.1 centimeters across 13 acres

## The Construction Challenge

Here's what keeps historians and engineers up at night: We still don't fully understand how it was built.

Consider the logistics:
- **Construction time:** Approximately 20 years
- **Daily rate:** That works out to 315 blocks placed per day
- **Hourly rate:** 12-13 blocks per hour
- **Per block:** One block every 4-5 minutes, around the clock

Each block had to be:
1. Quarried from bedrock
2. Cut to precise dimensions
3. Transported to the site (some from 800 km away)
4. Lifted into position
5. Aligned perfectly with its neighbors

And they did this with copper tools, wooden sledges, and rope made from papyrus. No wheels for construction. No iron or steel. No cranes or pulleys as we know them.

## What We Know vs. What We Don't

**What archaeology has confirmed:**
- The pyramid was built during Pharaoh Khufu's reign (circa 2560 BCE)
- A skilled workforce of 20,000-30,000 people built it (not slaves)
- Workers were well-fed, received medical care, and lived in nearby villages
- Multiple types of stone were used from different quarries

**What remains mysterious:**
- The exact construction method (ramps? levers? combination?)
- How they achieved such precision without modern surveying tools
- The purpose of internal shafts that don't reach the outside
- Whether there are still undiscovered chambers
- Why the King's Chamber sarcophagus was found empty

## Why It Still Matters

The Great Pyramid isn't just an ancient monument - it's proof of what humans can achieve. Before modern machinery, computers, or even basic metal tools, our ancestors built something that still astounds engineers today.

When you stand before it, you're not just looking at old stones. You're looking at the organized effort of an entire civilization, the mathematical knowledge of ancient minds, and a testament to human ambition that has endured for 4,500 years.

---

*This is Part 1 of our 9-part series on the Great Pyramid of Giza. Follow along as we uncover every secret, debunk every myth, and explore humanity's greatest architectural achievement.*
'''
        },
        {
            'title': 'Building the Great Pyramid: Timeline, Workers, and the 20-Year Challenge',
            'slug': 'great-pyramid-history-timeline-workers',
            'excerpt': "How long did it take to build the Great Pyramid? Who were the workers? Explore the complete timeline and discover the truth about the builders of Egypt's greatest monument.",
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',
            'meta_description': 'Learn the true history of the Great Pyramid construction - 20 years, 30,000 workers, and incredible organization. Not slaves, but skilled craftsmen.',
            'meta_keywords': 'pyramid construction, khufu, pyramid workers, ancient egypt history, pyramid timeline',
            'tags': 'pyramid history, construction, workers, timeline, khufu',
            'is_featured': False,
            'content': '''## When Was the Great Pyramid Built?

The Great Pyramid was constructed during the reign of Pharaoh Khufu (also known by his Greek name, Cheops), the second pharaoh of the Fourth Dynasty of Egypt's Old Kingdom. Based on archaeological evidence and historical records, construction began around 2560 BCE - approximately 4,584 years ago.

## The Timeline of Construction

### Before Construction Began

The pyramid wasn't built on a whim. Years of planning preceded the first stone:

- **Site selection:** The Giza Plateau was chosen for its solid bedrock and proximity to the Nile
- **Surveying:** The base had to be perfectly level across 13 acres
- **Quarry preparation:** Limestone quarries needed to be established
- **Logistics planning:** Housing, food, and supply chains for thousands of workers
- **Road building:** Causeways for transporting stones from quarries

### The Construction Period

Based on the evidence, the Great Pyramid took approximately **20-27 years** to complete - essentially the entirety of Khufu's reign.

Let's break down what that means mathematically:

| Metric | Calculation |
|--------|-------------|
| Total blocks | ~2,300,000 |
| Construction years | 20 |
| Working days per year | ~365 |
| Total days | ~7,300 |
| Blocks per day | ~315 |
| Blocks per hour (24-hour) | ~13 |
| Time per block | ~4.6 minutes |

For 20 years straight, a 2.5-ton block was placed every 5 minutes, around the clock.

## Who Built the Pyramids?

### The Slave Myth - Debunked

One of the most persistent myths about the pyramids is that they were built by Hebrew slaves. This is **not supported by archaeological evidence**.

**What we've actually found:**

1. **Worker villages:** In 1990, archaeologists discovered the remains of a worker city near the pyramids. These weren't slave quarters - they were organized communities.

2. **Evidence of good treatment:**
   - Bakeries capable of producing thousands of loaves daily
   - Breweries (beer was a staple food in ancient Egypt)
   - Medical facilities showing healed bones - workers received care for injuries
   - Butcher shops with cattle bones - they ate meat, a luxury

3. **Graffiti with pride:** Workers left graffiti on blocks like "Friends of Khufu Gang" and "Drunkards of Menkaure" - not the words of enslaved people

4. **Proper burials:** Workers' cemeteries have been found with proper burial rites - slaves would not have received such treatment

### The Actual Workforce

The Great Pyramid was built by:

**Permanent Skilled Workers (2,000-5,000)**
- Stone masons and cutters
- Engineers and architects
- Surveyors
- Overseers and administrators
- Ramp builders

**Rotating Labor Force (20,000-30,000)**
- Farmers who worked during the Nile's flood season (when farming was impossible)
- This was essentially a form of tax payment
- Workers rotated in 3-month shifts
- They were fed, housed, and likely proud to participate

### The Organization

The workforce was organized into crews (called "phyles") of about 2,000 men each. These were divided into smaller groups:

- **Gangs:** ~200 workers each
- **Divisions:** 20 workers each

Each group had leaders, and there was a clear hierarchy. This wasn't chaos - it was the most organized construction project of the ancient world.

## The Legacy

When the last stone was placed, the workers had created something that would outlast every other structure of its time. They couldn't have known that 4,500 years later, their work would still stand - still inspiring wonder, still keeping secrets.

The Great Pyramid is more than stone. It's a monument to human organization, determination, and skill.

---

*Part 2 of 9 in our Great Pyramid series. Next: The impossible precision of the pyramid's architecture.*
'''
        },
        {
            'title': "The Architecture of the Great Pyramid: Precision That Shouldn't Exist",
            'slug': 'great-pyramid-architecture-precision',
            'excerpt': "The Great Pyramid's precision rivals modern engineering - 99.98% symmetrical, aligned to true north, level to 2cm across 13 acres. All without lasers, computers, or modern tools.",
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
            'meta_description': 'Discover the impossible precision of the Great Pyramid - architectural accuracy that challenges what we think ancient people could achieve.',
            'meta_keywords': 'pyramid architecture, pyramid precision, ancient engineering, pyramid design, giza measurements',
            'tags': 'architecture, precision, engineering, design, measurements',
            'is_featured': False,
            'content': '''## Precision That Challenges Understanding

The Great Pyramid of Giza wasn't just big - it was impossibly precise. The level of accuracy achieved by ancient Egyptian builders rivals, and in some cases exceeds, modern construction standards.

## Base Measurements

### The Four Sides

Each side of the pyramid's base measures approximately 230.4 meters (755.9 feet). But it's the consistency that's remarkable:

| Side | Length | Difference from Mean |
|------|--------|---------------------|
| North | 230.253 m | -0.147 m |
| South | 230.454 m | +0.054 m |
| East | 230.391 m | -0.009 m |
| West | 230.357 m | -0.043 m |

**Maximum difference between sides: 4.4 centimeters (1.7 inches)**

That's **99.98% perfect symmetry** across a base covering 13 acres. Many modern buildings don't achieve this level of precision.

### Level Ground

The base of the pyramid is level to within **2.1 centimeters** (less than 1 inch) across the entire 230-meter span. This is remarkable for several reasons:

1. The bedrock is naturally uneven
2. They had no laser levels
3. The margin of error is smaller than a golf ball

**How they likely did it:** By cutting channels in the bedrock, filling them with water (which naturally finds level), and using the waterline as a reference.

## True North Alignment

The Great Pyramid is aligned to true north with an error of only **3/60ths of a degree** (0.05 degrees).

### Why This Matters

- The compass wasn't invented until 2,300 years later
- They had to determine true north through astronomical observation
- This is more accurate than the Royal Greenwich Observatory
- Modern buildings are rarely aligned this precisely

### How They Probably Did It

The Egyptians likely used stellar observation:

1. Tracked the movement of circumpolar stars
2. Marked where a star set and rose on the horizon
3. Split the difference to find true north
4. Verified with multiple observations over time

## Corner Angles

The four corner angles of the pyramid are almost exactly 90 degrees:

| Corner | Angle | Error |
|--------|-------|-------|
| NE | 90deg 3' 2" | +3' 2" |
| NW | 89deg 59' 58" | -0' 2" |
| SE | 89deg 56' 27" | -3' 33" |
| SW | 90deg 0' 33" | +0' 33" |

The average error is approximately **2 arc-minutes** - a level of precision difficult to achieve even with modern tools without careful measurement.

## Stone Fitting Precision

The casing stones (the outer layer) were cut and fitted with extraordinary precision:

- **Joint width:** Less than 0.5 millimeters in many places
- **Test:** You cannot fit a piece of paper between many stones
- **Comparison:** This is more precise than modern machine cutting for many applications

### The Casing Stones

The pyramid was originally covered in white Tura limestone:
- Polished to a mirror-like finish
- Would have gleamed brilliantly in the sun
- Most were stripped for other construction projects
- Some remain at the base of the pyramid

## How Did They Do It?

### Tools Available
- Copper chisels and saws
- Wooden set squares
- Plumb bobs for vertical alignment
- String stretched between points
- Water for leveling
- Careful astronomical observation

### Tools NOT Available
- Iron or steel tools
- The compass
- Modern surveying equipment
- Laser levels
- Computer-aided design

The Great Pyramid stands as proof that ancient peoples were not primitive. They possessed sophisticated mathematical knowledge, astronomical understanding, and engineering capabilities that demand our respect.

---

*Part 3 of 9 in our Great Pyramid series. Next: Inside the pyramid - exploring the mysterious King's Chamber.*
'''
        },
        {
            'title': "The King's Chamber: Heart of the Great Pyramid",
            'slug': 'great-pyramid-kings-chamber-secrets',
            'excerpt': "Deep inside the Great Pyramid lies the King's Chamber - built of granite from 800km away, with an empty sarcophagus and mysterious shafts. Discover its secrets.",
            'image_url': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200&q=80',
            'meta_description': 'Explore the King\'s Chamber inside the Great Pyramid - granite construction, mysterious air shafts, and an empty sarcophagus that raises more questions than answers.',
            'meta_keywords': 'kings chamber, great pyramid interior, pyramid sarcophagus, pyramid shafts, khufu tomb',
            'tags': 'kings chamber, interior, sarcophagus, shafts, mysteries',
            'is_featured': False,
            'content': '''## The Heart of the Great Pyramid

Forty-three meters above ground level, deep within the Great Pyramid's stone mass, lies the King's Chamber - the supposed final resting place of Pharaoh Khufu. It is perhaps the most mysterious room ever built.

## Location and Access

### The Journey Inside

To reach the King's Chamber, you must navigate:

1. **The Original Entrance** - Located on the north face, 17 meters above ground, hidden for millennia

2. **The Descending Corridor** - Slopes downward into the bedrock, leads to the underground chamber (a decoy?)

3. **The Ascending Corridor** - Hidden junction with the descending corridor, blocked by massive granite plugs

4. **The Grand Gallery** - 47 meters long, 8.5 meters high, one of the most impressive interior spaces in any ancient structure

5. **The Antechamber** - Contains grooves for three portcullis slabs meant to seal the chamber after burial

6. **The King's Chamber** - The final destination, a room like no other

## The Chamber Itself

### Dimensions

| Measurement | Metric | Imperial |
|-------------|--------|----------|
| Length | 10.47 m | 34.4 ft |
| Width | 5.23 m | 17.2 ft |
| Height | 5.82 m | 19.1 ft |

Note the length is exactly twice the width - a 2:1 ratio that appears deliberately mathematical.

### Construction Material

Unlike the rest of the pyramid (limestone), the King's Chamber is built entirely of **red granite**:

- Quarried in Aswan, 800 kilometers south
- Transported by boat down the Nile
- Some of the hardest stone available in ancient Egypt

### The Ceiling

Above the chamber are **nine massive ceiling beams**:

- Each beam spans the full width of the room
- Weight: 25 to 80 tons each
- Total weight of ceiling beams: approximately 400 tons
- Lifted 43 meters into the air during construction

## The Sarcophagus

### Physical Description

A rectangular granite sarcophagus sits against the western wall:

- **Material:** Red granite (like the chamber)
- **Weight:** Approximately 3.75 tons

### The Mystery

**The sarcophagus is too large to fit through the corridors.**

This means:
- It was placed in the chamber DURING construction
- The pyramid was literally built around it
- It was never meant to be removed

### The Discovery

When explorers first entered the King's Chamber (Al-Ma'mun in 820 CE), they found:
- The sarcophagus lid was missing
- The interior was empty
- No mummy, no treasure, no funerary goods
- Signs of ancient robbery? Or was it never used?

## The "Air Shafts"

Two shafts extend from the north and south walls of the King's Chamber:

### The Mystery

These shafts were long called "air shafts," but:
- They were originally **sealed** at both ends
- They don't provide ventilation
- They don't reach the outer surface of the pyramid
- Robots have explored them and found... sealed doors

### What's Behind the Doors?

In 1993 and 2002, robotic expeditions explored these shafts:
- Found small doors with copper handles
- Drilled through one door... found another door behind it
- What lies beyond remains unknown

---

*Part 4 of 9 in our Great Pyramid series. Next: How did they actually build it? Exploring construction theories.*
'''
        },
        {
            'title': 'How Was the Great Pyramid Built? Construction Methods Explained',
            'slug': 'great-pyramid-construction-methods',
            'excerpt': "No wheels, no cranes, no iron - how did ancient Egyptians build the Great Pyramid? Explore the leading theories: ramps, levers, and methods we're still debating.",
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
            'meta_description': 'How was the Great Pyramid built? Explore ramp theories, lever systems, and construction methods the ancient Egyptians may have used.',
            'meta_keywords': 'pyramid construction methods, how pyramids built, pyramid ramps, ancient construction, egyptian engineering',
            'tags': 'construction, methods, ramps, engineering, building',
            'is_featured': False,
            'content': '''## The Construction Mystery

Perhaps no question has puzzled historians, engineers, and curious minds more than this: How did the ancient Egyptians build the Great Pyramid?

With 2.3 million blocks, no wheels for heavy lifting, no iron or steel, and a construction timeline of approximately 20 years, the logistics seem impossible. Yet the pyramid stands - proof that somehow, they did it.

## What We Know They Had

### Tools and Materials

**Cutting Tools:**
- Copper chisels (copper was the hardest metal available)
- Copper saws
- Dolerite pounders (harder stone for working granite)

**Lifting and Moving:**
- Wooden sledges
- Wooden rollers
- Levers (wooden beams)
- Rope made from papyrus and halfa grass

**Notable Absences:**
- No iron or steel
- No wheel for construction
- No pulleys (possibly)
- No cranes as we know them

## The Ramp Theories

Most Egyptologists agree ramps were essential. The debate is about what kind:

### Theory 1: Straight Ramp

A single ramp extending straight from the ground to the working level.

**Problems:**
- For a 7 degree slope to reach the top (146 m), the ramp would need to be **1.6 kilometers long**
- The ramp would contain more material than the pyramid itself

**Likelihood:** Possibly used for lower levels only

### Theory 2: Spiral External Ramp

A ramp that wraps around the pyramid, climbing as the structure grows.

**Evidence:**
- Corner notches found in the pyramid structure
- More practical than straight ramp
- Requires less material

**Likelihood:** Strong candidate, especially for middle sections

### Theory 3: Internal Ramp

A ramp built inside the pyramid itself, still existing within the structure.

**Proposed by:** French architect Jean-Pierre Houdin (2007)

**Evidence:**
- Thermal imaging shows unexplained internal structures
- Corner notches could be turning points
- Would explain how upper blocks were raised

**Likelihood:** Intriguing theory, needs more evidence

## The Water Element

### Wet Sand Discovery

In 2014, physicists confirmed what an ancient Egyptian painting seemed to show:

**The experiment:**
- Dry sand creates significant friction
- Wet sand (with correct moisture) reduces friction by up to 50%
- A sledge glides much more easily on wet sand

**The painting:**
- A wall painting from Djehutihotep's tomb (circa 1900 BCE)
- Shows a worker pouring water in front of a sledge
- Long dismissed as ceremonial
- Now understood as practical engineering

## The Combined Answer

Most modern Egyptologists believe:

1. **Lower section (bottom ~30%):** Straight ramp from local quarry
2. **Middle section:** External spiral ramp or internal ramp
3. **Upper section:** Lever systems, internal ramp, or combination
4. **Throughout:** Wet sand lubrication, organized labor crews

The Great Pyramid wasn't built with one method - it was built with Egyptian ingenuity, adapting techniques as challenges changed.

---

*Part 5 of 9 in our Great Pyramid series. Next: Cutting 2.3 million stones with copper tools.*
'''
        },
        {
            'title': 'Cutting Pyramid Stones: How Did They Do It With Copper Tools?',
            'slug': 'great-pyramid-stone-cutting',
            'excerpt': "The Great Pyramid's stones are cut so precisely you can't fit paper between them - yet they only had copper tools. Discover the ancient techniques of stone cutting.",
            'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200&q=80',
            'meta_description': 'How did ancient Egyptians cut 2.3 million perfectly shaped stones with copper tools? Explore the quarrying techniques and precision that built the Great Pyramid.',
            'meta_keywords': 'pyramid stones, stone cutting ancient egypt, quarrying pyramids, copper tools egypt, pyramid construction',
            'tags': 'stones, cutting, quarrying, copper tools, precision',
            'is_featured': False,
            'content': '''## The Stone Cutting Challenge

The Great Pyramid contains approximately 2.3 million stone blocks. Each block was quarried, shaped, transported, and fitted so precisely that in many places, you cannot insert a sheet of paper between them.

They did this with copper tools.

## The Quarries

Stone for the Great Pyramid came from three main sources:

### 1. Local Limestone Quarry (300 meters away)

**What:** The bulk of the pyramid (roughly 70%)
**Stone type:** Nummulitic limestone
**Distance:** Just 300 meters south of the pyramid
**Use:** Core blocks (interior of pyramid)

### 2. Tura Quarries (15 km across the Nile)

**What:** The outer casing stones
**Stone type:** Fine white limestone
**Distance:** 15 kilometers across the Nile River
**Use:** Polished exterior (the "shining" surface)

### 3. Aswan Quarries (800 km south)

**What:** The hardest stones - granite
**Stone type:** Red and gray granite
**Distance:** 800 kilometers up the Nile
**Use:** King's Chamber, sarcophagus, relieving chambers

## Cutting Limestone

### The Process

**Step 1: Marking**
- Surveyors marked the block dimensions on the quarry face
- Red ochre was used for marking lines

**Step 2: Cutting Grooves**
- Workers cut grooves around the block using copper chisels
- Grooves were approximately 10-15 cm deep

**Step 3: The Wedge Technique**
- Wooden wedges inserted into the grooves
- Wedges placed along the entire cut line

**Step 4: Adding Water**
- Water poured onto the wooden wedges
- Wood absorbed water and expanded
- Expansion created tremendous pressure
- Stone cracked along the desired line

**Step 5: Extraction**
- The freed block was levered out
- Rough shaping done at the quarry
- Final shaping done at the pyramid site

## Cutting Granite

This is where it gets mysterious.

### The Problem

Granite from Aswan was used for the King's Chamber:

**Granite hardness:** 6-7 on Mohs scale
**Copper hardness:** 3 on Mohs scale

**You cannot cut granite with copper.** The tool will wear away before the stone does.

### Theories for Granite Cutting

**Theory 1: Dolerite Pounders**
- Dolerite is harder than granite
- Workers pounded the granite with dolerite balls
- Evidence: Dolerite balls found at quarry sites

**Theory 2: Abrasive Cutting**
- Copper saws used with sand as abrasive
- The sand, not the copper, does the cutting
- Evidence: Saw marks found on granite blocks

## The Precision

### Casing Stone Accuracy

| Measurement | Value |
|-------------|-------|
| Joint width | < 0.5 mm in many places |
| Surface flatness | Within 1/50th of an inch |
| Angle consistency | Uniform across all stones |

This is comparable to or exceeds modern precision cutting.

---

*Part 6 of 9 in our Great Pyramid series. Next: Moving 2.3 million blocks - the transportation challenge.*
'''
        },
        {
            'title': 'Moving Pyramid Stones: Transporting 2.3 Million Blocks Without Wheels',
            'slug': 'great-pyramid-transporting-stones',
            'excerpt': "How did the Egyptians move 80-ton blocks 800 kilometers without trucks or cranes? Discover the ingenious techniques of Nile transport and the wet sand secret.",
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
            'meta_description': 'How did ancient Egyptians transport pyramid stones weighing up to 80 tons? Discover the Nile waterway system, wet sand lubrication, and massive workforce coordination.',
            'meta_keywords': 'pyramid transport, moving pyramid stones, ancient egypt logistics, pyramid construction, nile transport',
            'tags': 'transport, moving stones, nile, logistics, engineering',
            'is_featured': False,
            'content': '''## The Transportation Challenge

Building the Great Pyramid wasn't just about cutting stones - it was about moving them. Some blocks weighed up to 80 tons. Some came from 800 kilometers away. None could be moved with trucks, cranes, or even wheels as we know them.

Yet they moved 2.3 million of them.

## Moving Local Limestone

### The Short Journey (300 meters)

Most of the pyramid's mass came from a quarry just 300 meters south.

**The Process:**
1. Block freed from bedrock
2. Basic dimensions cut at quarry
3. Block placed on wooden sledge
4. Road to construction site prepared
5. Teams of workers pulled the sledge
6. Block positioned for lifting

### The Wet Sand Revolution

For decades, scientists wondered how Egyptians moved such heavy blocks. The answer came from an ancient painting and modern physics.

**The Ancient Evidence:**

A wall painting from the tomb of Djehutihotep (c. 1900 BCE) shows:
- A massive statue on a sledge
- 172 workers pulling with ropes
- One worker standing at the front
- **Pouring water onto the sand ahead of the sledge**

**The Scientific Proof (2014):**

| Condition | Friction Level |
|-----------|----------------|
| Dry sand | High - sledge digs in and stops |
| Too wet | High - sledge creates wave of mud |
| Optimal moisture (2-5%) | **50% reduction in friction** |

With properly moistened sand:
- A 2.5-ton block: 20-40 workers could pull it
- Much less effort than previously thought

## Moving Granite from Aswan

### The Long Journey (800 kilometers)

The King's Chamber is built from red granite quarried in Aswan - 800 kilometers south of Giza.

### Nile Transportation

**The journey:**
- 800 kilometers downstream (north)
- Current assists the journey
- Special cargo vessels built for heavy loads

**Timing:**
- Annual Nile flood (July-October)
- Higher water = easier navigation
- Deeper channels = heavier loads possible

**The Fleet:**
- Purpose-built cargo boats
- Up to 50 meters long
- Made from Lebanese cedar

## The King's Chamber Challenge

The most impressive lifting achievement:

**The granite ceiling beams:**
- 9 beams
- Weight: 25-80 tons each
- Height: 43 meters above ground
- Had to be lifted with precision

How this was accomplished remains one of the great mysteries.

## The Real Achievement

The technology wasn't complex - sledges, ropes, water, and human power. The achievement was in the organization:

- **Logistics:** Moving right blocks to right place at right time
- **Coordination:** Thousands of workers acting in unison
- **Sustained effort:** Maintaining operation for 20 years
- **Quality control:** Ensuring every block fit perfectly

---

*Part 7 of 9 in our Great Pyramid series. Next: Debunking the myths - aliens, slaves, and misconceptions.*
'''
        },
        {
            'title': 'Great Pyramid Myths Debunked: Aliens, Slaves, and Misconceptions',
            'slug': 'great-pyramid-myths-debunked',
            'excerpt': "Aliens didn't build the pyramids. Slaves didn't either. Let's debunk the most persistent myths about the Great Pyramid and reveal what the evidence actually shows.",
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',
            'meta_description': "Debunking Great Pyramid myths: Were slaves involved? Did aliens help? Could we build it today? Get the facts based on archaeological evidence.",
            'meta_keywords': 'pyramid myths, aliens pyramids, pyramid slaves, pyramid facts, debunking pyramids',
            'tags': 'myths, debunked, facts, aliens, slaves, truth',
            'is_featured': False,
            'content': '''## Separating Fact from Fiction

Few ancient structures have generated more myths than the Great Pyramid. From claims of alien intervention to assumptions about slave labor, misinformation abounds.

---

## Myth #1: "Slaves Built the Pyramids"

### The Myth
The image of whip-cracking overseers forcing Hebrew slaves to drag blocks through the desert is iconic - and wrong.

### The Truth

**Archaeological Evidence:**

In 1990, archaeologists discovered the workers' village near the pyramids:

**Housing:**
- Organized dormitories and family houses
- Not slave quarters - proper accommodations

**Food:**
- Bakeries producing thousands of loaves daily
- Breweries (beer was a dietary staple)
- Workers ate meat - a luxury in ancient Egypt

**Medical Care:**
- Skeletal remains show healed bones
- Injured workers received care

**Graffiti:**
- Workers left graffiti like "Friends of Khufu Gang"
- These are not the words of enslaved people

**Burials:**
- Workers buried in tombs near the pyramids
- Proper burial rites observed
- Slaves would never receive such treatment

---

## Myth #2: "Aliens Built the Pyramids"

### The Myth
Ancient humans couldn't have built something so precise. Therefore, extraterrestrials must have helped.

### The Truth

This myth is not only wrong - it's insulting to ancient Egyptian achievement.

**The Evidence Against Aliens:**

1. **We have the quarries** - The source of the blocks is known
2. **We have the tools** - Copper chisels found at sites
3. **We have the worker villages** - Human, not alien
4. **We have progressive development** - Earlier pyramids show experimentation
5. **We have records** - Administrative documents and graffiti

**The Truth:**
Ancient Egyptians were brilliant engineers. Their precision astounds us because we underestimate them.

---

## Myth #3: "We Couldn't Build It Today"

### The Myth
Modern technology couldn't replicate the Great Pyramid.

### The Truth
We absolutely could build it today. We choose not to.

**Evidence:**
- 1978: A Japanese team built a small pyramid using ancient methods
- Modern cranes could lift the heaviest blocks with ease
- Computer modeling could replicate the precision exactly

**Why We Don't:**
- Cost would be billions of dollars
- No practical purpose
- Takes years of effort

---

## Myth #4: "20 Years is Impossible"

### The Truth
It's challenging math, but not impossible.

**The Calculation:**
- 2.3 million blocks / 20 years = 115,000 blocks per year
- 115,000 / 365 days = 315 blocks per day
- With 20,000 organized workers
- Multiple operations running simultaneously

Is it easy? No. Is it impossible? Also no.

---

## What We Can Learn

1. **Don't underestimate ancient peoples** - They were as intelligent as us
2. **Evidence matters** - Archaeological evidence trumps speculation
3. **Simple doesn't mean easy** - Basic technology + brilliant organization = extraordinary results

---

*Part 8 of 9 in our Great Pyramid series. Next: Why did they build it? The purpose and meaning of the Great Pyramid.*
'''
        },
        {
            'title': 'Why Was the Great Pyramid Built? Purpose, Meaning, and Mysteries',
            'slug': 'great-pyramid-purpose-meaning',
            'excerpt': "The Great Pyramid took 20 years and millions of blocks. But why? Explore the official purpose, deeper meanings, and enduring mysteries of humanity's greatest monument.",
            'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200&q=80',
            'meta_description': 'Why was the Great Pyramid built? Explore the tomb theory, astronomical alignments, national unity, and the mysteries that remain after 4,500 years.',
            'meta_keywords': 'pyramid purpose, why pyramids built, pyramid meaning, khufu tomb, ancient egypt beliefs',
            'tags': 'purpose, meaning, tomb, afterlife, mysteries, legacy',
            'is_featured': False,
            'content': '''## The Ultimate Question

After exploring how the Great Pyramid was built, we arrive at the most profound question: Why?

Why did an entire civilization dedicate 20 years and incalculable resources to building a single structure?

## The Official Purpose: A Tomb for Eternity

### Ancient Egyptian Beliefs

To understand the pyramid, we must understand Egyptian beliefs about death:

**The Pharaoh's Divine Status:**
- The pharaoh was not merely a king
- He was a living god on Earth
- Would become Osiris after death
- Served as intermediary between gods and people

**Death as Transition:**
- Death was not an end but a journey
- The soul continued to exist
- The body must be preserved
- A proper tomb ensured eternal life

### Why a Pyramid Shape?

**Religious Symbolism:**
- Represented the primordial mound from which all creation arose
- Pointed toward the sun (Re, the sun god)
- Created a "stairway to heaven" for the soul's ascent
- The shape mimics the rays of the sun through clouds

## Beyond the Tomb: Additional Purposes

### 1. National Unity

- United all of Egypt in a common purpose
- Farmers worked during flood season
- Shared experience created national identity

### 2. Political Power Statement

- Demonstrated Egypt's organizational capability
- Showed the pharaoh's absolute power
- A permanent reminder of the ruler's glory

### 3. Economic Engine

- Employed tens of thousands for decades
- Developed infrastructure
- Advanced technology and techniques

## The Astronomical Dimension

### Celestial Alignments

| Shaft | Points Toward | Significance |
|-------|--------------|--------------|
| Southern (King's) | Orion's Belt | Osiris, god of the dead |
| Northern (King's) | Thuban (pole star) | Celestial pole |
| Southern (Queen's) | Sirius | Isis, consort of Osiris |

## The Mysteries That Remain

### The Empty Sarcophagus

When the King's Chamber was first entered (820 CE):
- No mummy inside
- No treasure or funerary goods
- No evidence of what happened

### The "Air Shafts"

- Were sealed at both ends
- Don't reach the outer surface
- Robots found sealed doors with copper handles
- Behind one door... another door
- What lies beyond remains unknown

### Hidden Chambers

- Thermal imaging shows unexplained voids
- A large cavity above the Grand Gallery was detected in 2017
- The pyramid may still hold secrets

## The Enduring Legacy

Whatever its original purpose, the Great Pyramid has become something more:

**A Testament to Human Ambition:**
- Built with simple tools through sheer determination
- Still standing after millennia
- Still inspiring wonder

## Conclusion

The Great Pyramid was built so that a king could live forever.

In a way, it worked.

Khufu's name has survived 45 centuries. His monument attracts millions of visitors. His achievement still inspires researchers, engineers, and dreamers worldwide.

4,500 years ago, people with copper tools and rope built a mountain of stone so precise it challenges modern understanding. If they could do that, what are we capable of?

That, perhaps, is the greatest legacy of the Great Pyramid.

---

*Final article (Part 9 of 9) in our Great Pyramid series. The wonder continues.*
'''
        },
    ]

    for article in articles:
        BlogPost.objects.update_or_create(
            slug=article['slug'],
            defaults={
                'title': article['title'],
                'author': author,
                'category': category,
                'excerpt': article['excerpt'],
                'content': article['content'],
                'image_url': article['image_url'],
                'meta_description': article['meta_description'],
                'meta_keywords': article['meta_keywords'],
                'tags': article['tags'],
                'status': 'published',
                'is_featured': article['is_featured'],
                'published_at': now,
            }
        )


def reverse_pyramid_articles(apps, schema_editor):
    """Remove the seeded pyramid articles."""
    BlogPost = apps.get_model('blog', 'BlogPost')
    slugs = [
        'great-pyramid-giza-introduction',
        'great-pyramid-history-timeline-workers',
        'great-pyramid-architecture-precision',
        'great-pyramid-kings-chamber-secrets',
        'great-pyramid-construction-methods',
        'great-pyramid-stone-cutting',
        'great-pyramid-transporting-stones',
        'great-pyramid-myths-debunked',
        'great-pyramid-purpose-meaning',
    ]
    BlogPost.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_seed_city_guides'),
    ]

    operations = [
        migrations.RunPython(create_pyramid_articles, reverse_pyramid_articles),
    ]
