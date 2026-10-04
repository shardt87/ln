"""Page copy for the one-page leave-behinds (no bpy dependency).

Every page uses the same structure.  `view` names the saved camera / visibility
preset in the master .blend.  Callout labels (short, on the render) match the
three numbered opportunity statements below the render.

These are discussion concepts.  Nothing here states or implies that a company
has agreed to a partnership, pilot or purchase, and no performance numbers are
claimed.
"""

COMMON = {
    "brand": "Southwire",
    "unit": "Power Generation Solutions",
    "established": "Established: Southwire wire and cable manufacturing and supply.",
    "proposed": ("For evaluation: the prepared kits, cable packages and assemblies shown are application "
                 "concepts, not qualified Southwire products."),
    "disclaimer": ("Illustrative model. Ratings, cable sizes, clearances and termination selections are subject "
                   "to application engineering. No code compliance, engineering approval or certification is implied."),
    "contact_name": "Stephan Hardt",
    "contact_title": "Director, Power Generation Solutions, Southwire",
    "contact_phone": "[Phone]",
    "contact_email": "[Email]",
    "legend": [("Wire_Control", "Control wiring (presentation blue)"),
               ("Jacket_Power", "Power conductors"),
               ("Wire_Ground", "Grounding / bonding"),
               ("Highlight_Field", "Completed onsite (presentation amber)")],
    "legend_note": "Highlight colors are for presentation only and do not indicate conductor identification.",
}

PAGES = [
    {
        "key": "IEM", "company": "IEM", "view": "IEM_ControlKit",
        "headline": "Prepared wiring kits for switchgear production",
        "support": ("Evaluate repeatable control wiring and internal cable assemblies against your equipment "
                    "design and production process."),
        "callouts": ["Prepared and identified conductors", "Kits organized by cubicle or assembly step",
                     "Defined inspection, testing, and traceability requirements"],
        "statements": [
            "Cut to length, stripped and prepared for the illustrated terminals, with identification at both ends.",
            "Grouped and packed so each kit matches a section or build step instead of bulk wire at the bench.",
            "Inspection points, test methods and records agreed in advance and tied to each kit label.",
        ],
        "next": ("Review one representative wiring schedule and select a pilot assembly. Compare preparation "
                 "time, installation time, and rework with the current process."),
        "legend": ["Wire_Control", "Jacket_Power", "Wire_Ground"],
        "labels": {1: (0.38, 0.86, "L"), 2: (0.43, 0.59, "L"), 3: (0.955, 0.55, "L")},
        "legend_pos": "tr",
    },
    {
        "key": "CAT", "company": "Caterpillar Electric Power", "view": "CAT_GenInterface",
        "headline": "Cable packages for generator electrical interfaces",
        "support": ("Review where output leads, control wiring and external cable connections on a generator "
                    "platform could be prepared before final assembly."),
        "callouts": ["Terminal-box output leads", "Control and sensing wiring", "External cable interface"],
        "statements": [
            "Leads cut, terminated and identified to the terminal arrangement, compared with current preparation at assembly.",
            "Engine, regulator and remote-control conductors grouped by platform option and routed to a defined harness drawing.",
            "A defined hand-off at the cable exit: what the package supplies, what the installer connects, and how each is identified.",
        ],
        "next": ("Identify the engineering and sourcing owners for one generator platform and review its "
                 "terminal-box and control-wiring requirements together."),
        "legend": ["Wire_Control", "Jacket_Power", "Wire_Ground"],
        "labels": {1: (0.955, 0.64, "L"), 2: (0.955, 0.48, "L"), 3: (0.955, 0.30, "L")},
    },
    {
        "key": "TAYLOR", "company": "Taylor Power Systems", "view": "TAYLOR_GenKits",
        "headline": "Repeatable wiring packages for generator production",
        "support": ("Evaluate whether power leads and control wiring for recurring builds could arrive prepared, "
                    "identified and grouped for the assembly line."),
        "callouts": ["Power-lead kit", "Control-wire kit", "Build-specific identification"],
        "statements": [
            "Leads cut, terminated and labeled to the terminal-box layout of a recurring build, delivered as one set per unit.",
            "Conductors grouped by harness or assembly step, with identification at both ends and a packing list that matches the build sheet.",
            "Kit labels tied to the build record so material, revision and destination can be checked at the station.",
        ],
        "next": ("Review one recurring build and its wiring requirements. Compare current preparation, "
                 "installation and rework steps with a proposed kit."),
        "legend": ["Wire_Control", "Jacket_Power", "Wire_Ground"],
        "labels": {1: (0.10, 0.62, "R"), 2: (0.88, 0.62, "L"), 3: (0.28, 0.93, "R")}, "legend_pos": "br",
    },
    {
        "key": "EPD", "company": "Electronic Power Design", "view": "EPD_ControlCabinet",
        "headline": "Prepared wiring for paralleling and control equipment",
        "support": ("Evaluate repeatable control wiring in paralleling and control sections against your "
                    "schedules, devices and production sequence."),
        "callouts": ["Schedule-driven conductors", "Device and terminal-block landings", "Kits grouped by section"],
        "statements": [
            "Conductors cut, stripped, ferruled and marked from the wiring schedule, ready for termination at the panel.",
            "Preparation matched to the devices and terminal types used, following your termination practices.",
            "Kits packed per section or build step to fit the production sequence and limit sorting at the panel.",
        ],
        "next": ("Evaluate one wiring schedule from a recent paralleling or control section and select a "
                 "pilot assembly for comparison with the current process."),
        "legend": ["Wire_Control", "Jacket_Power", "Wire_Ground"],
        "labels": {1: (0.955, 0.43, "L"), 2: (0.18, 0.55, "R"), 3: (0.64, 0.95, "L")},
    },
    {
        "key": "POWELL", "company": "Powell", "view": "POWELL_EhouseExploded",
        "headline": "Interconnection packages for packaged electrical systems",
        "support": ("Examine the wiring and interconnections that cross shipping splits and are completed "
                    "after an electrical building is set."),
        "callouts": ["Factory-installed cable and tray", "Interconnect cable package", "Shipping-split field interface"],
        "statements": [
            "Cables routed and terminated within each shipping section before shipment, per the building design and its interconnection list.",
            "Split-crossing feeders and control cables prepared, identified and packed for the reconnection sequence.",
            "Tray splices, bonding jumpers and terminations defined so field work follows a known scope and a documented sequence.",
        ],
        "next": "Select one electrical package and walk through its interconnection list in an assembly review.",
        "legend": ["Jacket_Power", "Highlight_Field", "Wire_Ground"],
    },
    {
        "key": "PATRIOT", "company": "Patriot Switchgear", "view": "PATRIOT_Terminations",
        "headline": "Evaluating repetitive wire preparation in production",
        "support": ("Compare in-house cut, strip, ferrule and marking steps with conductors that arrive "
                    "prepared for the terminals you use."),
        "callouts": ["Identification at both ends", "Prepared ends for terminal blocks", "Lengths set by duct routing"],
        "statements": [
            "Markers printed to the wire list so each conductor can be checked against the schedule at installation.",
            "Strip lengths and ferrules selected for the terminal types used, subject to your termination standards.",
            "Lengths based on the routing through wire duct, keeping installation consistent from build to build.",
        ],
        "next": ("Compare current preparation steps with a proposed kit for one compartment, using the same "
                 "wiring schedule and terminal set."),
        "legend": ["Wire_Control", "Wire_Ground"],
    },
    {
        "key": "MAVERICK", "company": "Maverick Power", "view": "MAVERICK_Lineup",
        "headline": "Cable packages for custom power equipment",
        "support": ("Identify cable and wiring work in custom lineups that repeats often enough to prepare "
                    "before final assembly."),
        "callouts": ["Power-cable entry and landing", "Internal control wiring", "Grounding and bonding"],
        "statements": [
            "Incoming cables, lugs and identification planned to the lug pads, entry plates and bend space of each section.",
            "Repeatable control circuits prepared as kits, even where the lineup itself is custom.",
            "Ground leads and bonding jumpers cut and terminated to the equipment layout, including door and backplate bonds.",
        ],
        "next": ("Identify one generation-related manufacturing application where the wiring repeats and "
                 "review it as a candidate package."),
        "legend": ["Wire_Control", "Jacket_Power", "Wire_Ground"],
        "labels": {1: (0.40, 0.86, "L"), 2: (0.40, 0.35, "L"), 3: (0.955, 0.95, "L")}, "legend_pos": "tl",
    },
    {
        "key": "SIEMENS", "company": "Siemens Industry", "view": "SIEMENS_SkidBoundaries",
        "headline": "Defining interconnections for modular electrical skids",
        "support": ("Clarify which connections are completed in the factory and which are made after the "
                    "sections are placed onsite."),
        "callouts": ["Factory-installed connections", "Shipping-split boundary", "Site cable entry and grounding"],
        "statements": [
            "Cables routed and terminated within each section and checked before shipment, per the agreed plan.",
            "Split-crossing cables prepared, identified and staged to match the reconnection sequence.",
            "External feeders, cable transits and grounding pads defined as a clear site interface, with ownership agreed for each item.",
        ],
        "next": ("Review one skid interface and its installation sequence to identify which interconnections "
                 "could be prepared in advance."),
        "legend": ["Jacket_Power", "Highlight_Field", "Wire_Ground"],
        "labels": {1: (0.12, 0.20, "R"), 2: (0.45, 0.10, "R"), 3: (0.955, 0.22, "L")},
    },
    {
        "key": "ASCO", "company": "Schneider Electric / ASCO", "view": "ASCO_TransferInterface",
        "headline": "Defining scope at transfer-equipment interfaces",
        "support": ("Clarify factory-supplied and installer-supplied connections at the normal-source, "
                    "generator-source and load terminals. Open-transition switch shown; sources are not paralleled."),
        "callouts": ["Normal-source connection", "Generator-source connection", "Load connection"],
        "statements": [
            "Document lug, conductor and entry details so installer-supplied cable can be specified and prepared consistently.",
            "Evaluate prepared generator feeders and a separately routed engine-start control cable as one defined package.",
            "Confirm which load and neutral terminations are factory-supplied and which are completed by the installer.",
        ],
        "next": ("Establish factory-supplied versus installer-supplied scope for one transfer-switch "
                 "configuration and identify where a cable package could help."),
        "legend": ["Wire_Control", "Jacket_Power", "Wire_Ground"],
    },
    {
        "key": "INPOWER", "company": "InPower", "view": "INPOWER_Docking",
        "headline": "Generator docking and connection sets",
        "support": ("Review portable lead sets and internal docking-station wiring as coordinated, identified "
                    "connection packages."),
        "callouts": ["Portable lead sets", "Docking-station internal wiring", "Generator and load-bank ports"],
        "statements": [
            "Single-conductor sets built to length, with connectors and matching identification at both ends, stored as complete sets.",
            "Prepared conductors between receptacles, bus and disconnect, matched to the enclosure layout and installed as a kit.",
            "Separate generator-input and load-bank ports, with the facility feed treated as a fixed interface.",
        ],
        "next": ("Review one connection configuration, including ratings, connectors, lead lengths and "
                 "storage, as a candidate package."),
        "legend": ["Jacket_Power", "Wire_Ground"],
    },
    {
        "key": "NVENT", "company": "nVent", "view": "NVENT_EnclosureRouting",
        "headline": "Wiring and routing within enclosures and electrical buildings",
        "support": ("Evaluate how tray, cable entries and internal connections could be planned and supplied "
                    "together for an enclosure or building."),
        "callouts": ["Tray routing and segregation", "Cable entries and transits", "Internal equipment connections"],
        "statements": [
            "Power and control cables run in separate tray or channel, with routes defined before assembly.",
            "Entry plates and transits matched to the cable counts and sizes in the design, with spare capacity agreed up front.",
            "Equipment drops prepared to length and identified to the connection list, so each landing can be checked against the drawing.",
        ],
        "next": ("Select one enclosure or building application and define assembly ownership for tray, "
                 "entries and internal cabling."),
        "legend": ["Jacket_Power", "Highlight_Field", "Wire_Ground"],
        "labels": {1: (0.12, 0.18, "R"), 2: (0.955, 0.26, "L"), 3: (0.55, 0.12, "R")},
    },
    {
        "key": "MOSEBACH", "company": "Mosebach Load Banks", "view": "MOSEBACH_LoadBankTest",
        "headline": "Repeatable generator-testing connection sets",
        "support": ("Review the lead sets used to connect generators to load banks for testing, including "
                    "handling, storage and replacement."),
        "callouts": ["Generator-to-load-bank leads", "Configurable test load", "Lead-set storage and transport"],
        "statements": [
            "Portable sets with connectors, lengths and identification matched to the load bank connection panel and typical site layouts.",
            "The load bank is a configurable test load, connected through a dedicated port, not to facility loads.",
            "Coiled sets, labels and inspection records kept together for repeated deployments, with a defined point for retiring worn leads.",
        ],
        "next": "Review duty, ratings, connectors and replacement needs for one load-bank lead set.",
        "legend": ["Jacket_Power", "Wire_Ground"],
    },
    {
        "key": "RESA", "company": "RESA Power", "view": "RESA_TestBoundaries",
        "headline": "Cable assemblies coordinated with acceptance testing",
        "support": ("Align cable preparation, factory testing and field acceptance testing at a defined "
                    "equipment connection."),
        "callouts": ["Factory-tested equipment", "Site-installed cable boundary", "Field acceptance testing"],
        "statements": [
            "Transformer and switchgear terminations as delivered, with their factory test records and documented connection points.",
            "Cables and terminations installed onsite, prepared and identified for the defined connection points.",
            "Test methods, responsibilities and records agreed before installation rather than after, so results can be traced to each cable.",
        ],
        "next": ("Define one application, the responsibilities at each boundary and the acceptance criteria "
                 "for the cable connection."),
        "legend": ["Jacket_Power", "Highlight_Field", "Wire_Ground"],
        "labels": {1: (0.955, 0.72, "L"), 2: (0.55, 0.12, "R"), 3: (0.50, 0.93, "R")},
    },
    {
        "key": "WINAR", "company": "Winar Connection", "view": "WINAR_AssemblyBench",
        "headline": "Cable supply and assembly partnership",
        "support": ("Compare how cable supply, preparation, identification, testing and packaging could be "
                    "divided for a representative assembly."),
        "callouts": ["Cable and prepared end", "Termination and identification", "Inspection record and packaging"],
        "statements": [
            "Cable specification and preparation steps documented for one representative assembly, including strip lengths and tolerances.",
            "Lug selection, crimping tools and sleeve marking agreed per drawing and termination standard, with first-article review.",
            "Inspection and test record, packaging and labeling defined for each shipment, and responsibility assigned for each step.",
        ],
        "next": "Compare specifications, capacity and responsibilities for one representative assembly.",
        "legend": ["Jacket_Power"],
        "labels": {1: (0.04, 0.20, "R"), 2: (0.955, 0.84, "L"), 3: (0.88, 0.22, "L")}, "legend_pos": "tr",
    },
    {
        "key": "WESCO", "company": "Wesco", "view": "WESCO_StagedSupply",
        "headline": "Cable packages aligned with the build sequence",
        "support": ("Explore a coordinated supply approach where cable, reels and kits are staged to match the "
                    "equipment build or installation sequence."),
        "callouts": ["Equipment modules", "Labeled reels and kits", "Staged deliveries"],
        "statements": [
            "Each module or shipping section tied to its own cable and kit list, drawn from the equipment and installation drawings.",
            "Reels and kits identified to the program, section and installation step, so material can be checked on arrival.",
            "Deliveries planned against the build or installation sequence rather than one bulk shipment.",
        ],
        "next": "Identify one customer program where a coordinated supply approach could be evaluated.",
        "legend": ["Jacket_Power", "Highlight_Field"],
        "labels": {1: (0.12, 0.12, "R"), 2: (0.40, 0.82, "R"), 3: (0.62, 0.90, "R")},
    },
]
