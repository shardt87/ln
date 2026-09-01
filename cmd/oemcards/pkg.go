// The package -> parts map, ported verbatim from the handoff's oemcards.py.
// Key -> (name prefixes that ARE the package, camera az/el, pad ft, drop-roof).
// This is the part selection the README says to reuse: it tells the renderer
// exactly which parts make up "the HRSG", "the STG", "the MCC room" and so on.
package main

import "strings"

type pkgDef struct {
	Key      string
	Prefixes []string
	Az, El   float64 // degrees; az 0 = looking from +z, elevation up from horizon
	PadFt    float64
	DropRoof bool
}

var pkgs = []pkgDef{
	{"GT", []string{"GTG-01-gas-turbine", "GTG-01-compressor", "GTG-01-exhaust"}, 150, 24, 8, true},
	{"GEN", []string{"GTG-02-generator", "GTG-02-exciter", "GTG-02-terminal"}, 150, 24, 6, true},
	{"GTCTRL", []string{"GT-2-aux-fuelgas-valve-rack", "TC-MARSHALLING-GT2"}, 200, 26, 6, true},
	{"INLET", []string{"air-inlet-2-"}, 150, 22, 8, false},
	{"GTAUX", []string{"GT-2-aux-lube", "GT-2-aux-hydraulic", "GT-2-aux-fuelgas"}, 200, 26, 6, true},
	{"GTFIRE", []string{"FIRE-GT-2-"}, 200, 26, 5, true},
	{"HRSG", []string{"HRSG-2-"}, 150, 22, 10, false},
	{"CEMS", []string{"CEMS-HRSG-2-"}, 150, 20, 8, false},
	{"BFP", []string{"BFP-2-"}, 200, 26, 5, false},
	{"STG", []string{"STG-"}, 150, 24, 8, true},
	{"STAUX", []string{"ST-aux-", "STG-lube", "STG-ehc", "STG-gland", "STG-vacuum"}, 200, 26, 6, true},
	{"ACC", []string{"ACC-"}, 150, 24, 10, false},
	{"ACCFAN", []string{"ACC-fan-motor-4", "ACC-fan-motor-5", "ACC-fan-4", "ACC-fan-5"}, 200, 30, 5, false},
	{"ACCVFD", []string{"ELEC-ACC-VFD"}, 200, 26, 5, false},
	{"CEP", []string{"CEP-"}, 200, 26, 5, false},
	{"COOLTWR", []string{"cooling-tower-"}, 200, 26, 8, false},
	{"CWPUMP", []string{"pump-motor-", "pump-casing-", "pump-house"}, 200, 26, 6, false},
	{"CHILLER", []string{"chiller-"}, 200, 26, 6, false},
	{"GSU", []string{"transformer-0", "transformer-1", "transformer-2", "GSU-"}, 200, 26, 8, false},
	{"GCB", []string{"GCB-"}, 200, 26, 5, true},
	{"NGR", []string{"NGR-"}, 200, 26, 5, true},
	{"SWYARD", []string{"substation-breaker", "substation-disconnect", "substation-ct", "substation-cvt", "substation-arrester"}, 200, 28, 8, false},
	{"SUBCTRL", []string{"substation-control-house", "TRENCH-SUB"}, 200, 26, 6, false},
	{"MVSWGR", []string{"SWGR-MV-13800", "SWGR-MV-4160"}, 200, 26, 5, true},
	{"LVSWGR", []string{"SWGR-LV", "lv-panel"}, 200, 26, 5, true},
	{"MCC", []string{"MCC-A-", "MCC-B-", "MCC-hall-bay"}, 200, 26, 6, true},
	{"EHOUSE", []string{"ehouse"}, 200, 26, 6, false},
	{"VFD", []string{"VFD-"}, 200, 26, 5, true},
	{"UPS", []string{"UPS-A", "UPS-B"}, 200, 26, 5, true},
	{"DC", []string{"DC-CHARGER", "battery-"}, 200, 26, 5, true},
	{"DCS", []string{"admin-dcs-cabinet", "admin-console", "admin-mimic"}, 200, 26, 5, true},
	{"BESSCONT", []string{"BESS-container-0-1"}, 200, 26, 5, false},
	{"BESSPCS", []string{"ELEC-BESS-PCS-2"}, 200, 26, 5, false},
	{"BESSXFMR", []string{"ELEC-BESS-XFMR-2", "ELEC-BESS-COLLECTOR"}, 200, 26, 6, false},
	{"RICE", []string{"modular-unit-2"}, 200, 26, 6, false},
	{"BLACKST", []string{"blackstart-2"}, 200, 26, 5, false},
	{"FUELCELL", []string{"fuelcell-module", "fuelcell-skid"}, 200, 26, 5, false},
	{"FCPCS", []string{"fuelcell-inverter", "fuelcell-transformer", "ELEC-FUELCELL"}, 200, 26, 5, false},
	{"CCS", []string{"ccs-absorber", "ccs-dcc", "ccs-regen", "ccs-reboiler", "ccs-reflux"}, 200, 24, 10, false},
	{"CCSFAN", []string{"ccs-flue-fan", "ccs-pump", "ccs-cw"}, 200, 26, 6, false},
	{"LNGVAP", []string{"lng-vaporiser"}, 200, 26, 5, false},
	{"LNGPUMP", []string{"lng-pump", "lng-bog"}, 200, 26, 5, false},
	{"H2COMP", []string{"h2-compressor"}, 200, 26, 5, false},
	{"METERING", []string{"GMS-RUN-", "GMS-heater"}, 200, 26, 5, false},
	{"WWTP", []string{"WWTP-PACKAGE", "WWTP-CLARIFIER"}, 200, 26, 6, false},
	{"AIR", []string{"AIR-"}, 200, 26, 5, true},
	{"FIREGAS", []string{"GMS-LEL-", "GMS-GAS-DETECTION-PANEL"}, 200, 26, 5, false},
}

// Hall roof/shell parts dropped for interior packages.
var roofPrefixes = []string{
	"HALL-SECTION-FIXED-ROOF", "SECTIONCUT-HALL", "hall-roof", "HALL-FRAME-ROOF-BEAM",
}

func isRoof(name string) bool {
	return hasAnyPrefix(name, roofPrefixes)
}

// Below-grade parts to hide (site-base is translucent in the colour renders,
// so buried parts read through it): EXCAV-* / ZONE-* plus anything whose
// max y is below 0.05 ft — except site-base itself.
func isUnderground(p *Part) bool {
	if p.Name == "site-base" {
		return false
	}
	if hasAnyPrefix(p.Name, []string{"EXCAV-", "ZONE-"}) {
		return true
	}
	return p.Max[1]*mToFt < 0.05
}

// Ground context that is always kept regardless of the crop box.
func isGroundContext(name string) bool {
	return name == "site-base" || strings.Contains(name, "road") ||
		strings.Contains(name, "apron") || strings.HasSuffix(name, "-pad")
}

func hasAnyPrefix(name string, prefixes []string) bool {
	for _, p := range prefixes {
		if strings.HasPrefix(name, p) {
			return true
		}
	}
	return false
}
