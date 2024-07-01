POINT_SIZE = 10

# Supported labels
BC_D = [
    "TEMP",
    "UX",
    "UY",
    "UZ",
    "VOLT",  # "MAG"
]
BC_F = [
    "HEAT",
    "FX",
    "FY",
    "FZ",
    "AMPS",
    "CHRG",
    # "FLUX",
    "CSGZ",
]  # TODO: Add moments MX, MY, MZ
FIELDS = {
    "MECHANICAL": ["UX", "UY", "UZ", "FX", "FY", "FZ"],
    "THERMAL": ["TEMP", "HEAT"],
    "ELECTRICAL": ["VOLT", "CHRGS", "AMPS"],
}

FIELDS_ORDERED_LABELS = FIELDS["MECHANICAL"].copy()
FIELDS_ORDERED_LABELS.extend(FIELDS["THERMAL"])
FIELDS_ORDERED_LABELS.extend(FIELDS["ELECTRICAL"])

# All boundary conditions:
BCS = BC_D.copy()
BCS.extend(BC_F)

# Allowed entities to plot their boundary conditions
ALLOWED_TARGETS = ["NODES"]
