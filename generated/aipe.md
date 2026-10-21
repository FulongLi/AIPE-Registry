# AIPE — AI for Power Engineering

Generated from validated capability manifests. Open-source first, commercial compatible.

| Capability | Type | Maturity | Integration | Canonical repository |
| --- | --- | --- | --- | --- |
| AIPE Academy (`aipe.academy`) | education | prototype | mapped | [Repository](https://github.com/FulongLi/AIPE-Academy) |
| AIPE CAD Agent (`aipe.cad-agent`) | tool | prototype | none | [Repository](https://github.com/FulongLi/AIPE-CAD-Agent) |
| AIPE Core (`aipe.core`) | standard | prototype | native | [Repository](https://github.com/FulongLi/AIPE-Core) |
| AIPE Design Agent (`aipe.design-agent`) | agent | prototype | mapped | [Repository](https://github.com/FulongLi/AIPE-Design-Agent) |
| AIPE Doc (`aipe.doc`) | presentation | prototype | none | [Repository](https://github.com/FulongLi/AIPE-Doc) |
| AIPE Field Simulation (`aipe.field-simulation`) | tool | prototype | mapped | [Repository](https://github.com/FulongLi/AIPE-Field-Simulation) |
| AIPE IEEE Paper Agent (`aipe.ieee-paper-agent`) | agent | usable | mapped | [Repository](https://github.com/FulongLi/AIPE-IEEE-Paper-Agent) |
| AIPE Magnetics (`aipe.magnetics-database`) | tool | prototype | native | [Repository](https://github.com/FulongLi/AIPE-Magnetics-Database) |
| Open Engineering Tool Catalogue (`aipe.open-source-catalogue`) | catalogue | usable | none | [Repository](https://github.com/FulongLi/awesome-open-source-power-electronics) |
| AIPE Labs Presentation (`aipe.presentation`) | presentation | prototype | none | [Repository](https://github.com/FulongLi/Spirit-Connect-AIPE-Labs) |
| AIPE Registry (`aipe.registry`) | registry | prototype | none | [Repository](https://github.com/FulongLi/AIPE-Registry) |
| AIPE Semiconductor Database (`aipe.semiconductor-database`) | database | usable | mapped | [Repository](https://github.com/FulongLi/AIPE-Semiconductor-Database) |
| AIPE Simulation Skills (`aipe.simulation-skills`) | skill_collection | usable | mapped | [Repository](https://github.com/FulongLi/AIPE-Simulation-Skills) |
| AIPE Sketcher (`aipe.sketch`) | tool | usable | mapped | [Repository](https://github.com/FulongLi/AIPE-Sketcher) |
| AIPE Workflows (`aipe.workflows`) | agent | prototype | native | [Repository](https://github.com/FulongLi/AIPE-Workflows) |

## AIPE Academy

Original, AI-native Power and Energy Engineering curriculum in four domains (Foundations, Power Electronics, Power Systems, Renewable Energy) with reproducible Python labs, a verified MIT OpenCourseWare academic baseline, and a shared Codex skill / Claude Code plugin.

Capabilities: guided-engineering-education, open-source-converter-labs, reproducible-engineering-labs, academic-reference-baseline, codex-skill, claude-code-plugin.

Licence: `CC-BY-4.0`. Validation: `tested`.

- [Matplotlib](https://matplotlib.org/): open_source; optional; interfaces: python.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Most modules remain outlines or planned; one complete reference lesson exists per domain.
- Limitation: Labs are ideal analytical or numerical teaching models, not hardware validation.
- Limitation: The MIT OpenCourseWare baseline is a scope reference; AIPE Academy is not affiliated with or endorsed by MIT.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-Academy/blob/f4d8d4d4b35fc6de376c58afd127c43ba0fec20a/README.md)
- [Documentation: docs/architecture.md](https://github.com/FulongLi/AIPE-Academy/blob/f4d8d4d4b35fc6de376c58afd127c43ba0fec20a/docs/architecture.md)
- [Documentation: docs/curriculum-guide.md](https://github.com/FulongLi/AIPE-Academy/blob/f4d8d4d4b35fc6de376c58afd127c43ba0fec20a/docs/curriculum-guide.md)
- [Documentation: docs/plugin-installation.md](https://github.com/FulongLi/AIPE-Academy/blob/f4d8d4d4b35fc6de376c58afd127c43ba0fec20a/docs/plugin-installation.md)
- [Documentation: docs/website-integration.md](https://github.com/FulongLi/AIPE-Academy/blob/f4d8d4d4b35fc6de376c58afd127c43ba0fec20a/docs/website-integration.md)
- [Documentation: docs/ecosystem-v0.1.md](https://github.com/FulongLi/AIPE-Academy/blob/f4d8d4d4b35fc6de376c58afd127c43ba0fec20a/docs/ecosystem-v0.1.md)

## AIPE CAD Agent

Parametric FreeCAD geometry for power-converter transformers, plate-fin heat sinks, liquid cold plates and full converter assemblies, with STEP/FCStd export, mesh metadata and interference/clearance checks driven by JSON parameters in SI units.

Capabilities: parametric-transformer-cad, heat-sink-cad, cold-plate-cad, converter-assembly-cad, cad-interference-clearance-check.

Licence: `MIT`. Validation: `tested`.

- [CadQuery](https://cadquery.readthedocs.io/): open_source; optional; interfaces: python.
- [FreeCAD](https://www.freecad.org/): open_source; required; interfaces: cli, python.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Illustrative parametric models for layout, mass and clearance studies; not manufacturable designs and no DFM claims.
- Limitation: Windings are homogenised annular bodies with layer thickness derived from wire data; individual turns, lead-outs and bends are not modelled.
- Limitation: Clearance is measured as straight-line or one-bend air paths with Part.Shape.distToShape; creepage along insulating surfaces is not traced and conductors fully enclosed in insulation are reported for review.
- Limitation: Required clearance and creepage values are caller inputs; no compliance with any standard is asserted.
- Limitation: TDK E65/32/27 and Wolfspeed TO-247-4L dimensions are nominal values transcribed from the cited data sheets and must be verified against the current revisions.
- Limitation: No Engineering State adapter yet; integration with AIPE Core is planned, not implemented.
- Documentation staged locally (publication pending): `README.md`
- Documentation staged locally (publication pending): `docs/parameters.md`
- Documentation staged locally (publication pending): `examples/dab-10kw/README.md`

## AIPE Core

Versioned SI Engineering State schemas, evidence conventions and semantic interoperability contracts.

Capabilities: engineering-state-schema, engineering-evidence-contracts, offline-state-validation.

Licence: `MIT`. Validation: `tested`.

- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Schema and semantic checks do not prove engineering correctness or authenticate artifacts.
- Limitation: v0.1.0 schema URLs are logical identifiers until a release tag exists; resolve locally.
- Documentation staged locally (publication pending): `README.md`
- Documentation staged locally (publication pending): `docs/metadata.md`
- Documentation staged locally (publication pending): `docs/architecture-v0.1.md`
- Documentation staged locally (publication pending): `contracts/README.md`

## AIPE Design Agent

Incrementally orchestrate evidence-linked engineering work through Core state and Registry capabilities while retaining existing PEA calculators and interfaces.

Capabilities: engineering-orchestration, operating-point-analysis, converter-concept-calculation, dab-sps-analysis, thermal-cooling-screening.

Licence: `MIT`. Validation: `tested`.

- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Technical suitability and fidelity require an explicit assessment; metadata alone is not an engineering guarantee.
- Limitation: Only a built-in nominal operating-point adapter executes through the new orchestrator; other tools remain reviewable plans.
- Limitation: Existing PEA calculator/UI APIs remain separate from the additive Core state path.
- Limitation: pea.thermal results are analytical correlations (natural/forced convection, cold plate, spreading, Stage A Pareto screening) with stated validity ranges; they are not CFD, FEM or measured values and need the sibling HeatSinkOptimisation checkout.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-Design-Agent/blob/2d9c45fe3b70f6231fdda261c49555a245fd4306/README.md)
- [Documentation: docs/ecosystem-orchestration.md](https://github.com/FulongLi/AIPE-Design-Agent/blob/2d9c45fe3b70f6231fdda261c49555a245fd4306/docs/ecosystem-orchestration.md)
- [Documentation: pea/review/README.md](https://github.com/FulongLi/AIPE-Design-Agent/blob/2d9c45fe3b70f6231fdda261c49555a245fd4306/pea/review/README.md)
- [Documentation: CONTRIBUTING.md](https://github.com/FulongLi/AIPE-Design-Agent/blob/2d9c45fe3b70f6231fdda261c49555a245fd4306/CONTRIBUTING.md)

## AIPE Doc

AIPE-branded HTML document and slide templates (A4 and 16:9 print layouts) with shared stylesheets, a link/asset validator and a preview server; the engineering review package of AIPE-Workflows is rendered in the document layout.

Capabilities: engineering-document-templates, html-report-presentation.

Licence: `NOASSERTION`. Validation: `schema_validated`.

- [Node.js](https://nodejs.org/): open_source; optional; interfaces: cli.
- Limitation: check.mjs validates local links, ids and language pairs of the shipped templates; it does not validate engineering content.
- Limitation: PDF export relies on the browser print engine; no automated PDF generation is included.
- Limitation: Repository content has no declared licence (NOASSERTION); brand assets are AIPE Labs material.
- Documentation staged locally (publication pending): `README.md`
- Documentation staged locally (publication pending): `docs/guide.html`
- Documentation staged locally (publication pending): `templates/report-engineering.html`

## AIPE Field Simulation

Reproducible open-source field-simulation workflows (Gmsh meshing, ElmerGrid conversion, ElmerSolver FEM) for power-electronics thermal conduction, 2-D magnetostatics and 2-D eddy currents, with analytically verified benchmarks, mesh-convergence studies, DAB transformer-window and heat-sink parametric models, and AIPE evidence records (SI units, tool versions, SHA-256 artifacts).

Capabilities: fem-thermal-conduction, fem-magnetostatics-2d, fem-eddy-current-2d, analytic-benchmark-verification, simulation-case-provenance.

Licence: `MIT`. Validation: `tested`.

- [Elmer FEM (ElmerSolver, ElmerGrid)](https://www.elmerfem.org/): open_source; required; interfaces: cli, sif.
- [Gmsh](https://gmsh.info/): open_source; required; interfaces: python, cli.
- [OpenFOAM](https://www.openfoam.com/): open_source; optional; interfaces: cli.
- [Python](https://www.python.org/): open_source; required; interfaces: python, cli.
- Limitation: Tested means: unit tests of parsers/templating/analytic formulas plus end-to-end solver tests executed on Windows 11 with Gmsh 4.15.2 and Elmer 9.0; the solver tests skip when the tools are absent.
- Limitation: Benchmarks are verified against closed-form solutions only; no measured validation of any transformer or heat-sink result.
- Limitation: The transformer AC winding-loss factor uses a homogenised solid-block conductivity and is an approximation indicator, not a Litz/foil loss prediction; 3-D transformer models are not provided.
- Limitation: CFD (OpenFOAM) is blocked on this platform; heat-sink film coefficients are supplied values.
- Documentation staged locally (publication pending): `README.md`
- Documentation staged locally (publication pending): `results/benchmarks.md`
- Documentation staged locally (publication pending): `docs/jobs/openfoam-heatsink-cfd-job.md`
- Documentation staged locally (publication pending): `LICENSE`

## AIPE IEEE Paper Agent

Evidence-linked research planning and IEEE venue-specific manuscript production.

Capabilities: research-evidence-planning, ieee-manuscript-production.

Licence: `NOASSERTION`. Validation: `tested`.

- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Semantic Core mapping only; no automatic state converter.
- Limitation: Static checks do not verify citation truth or compile a PDF.
- Limitation: Repository-wide licence is unresolved; third-party assets retain rights.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-IEEE-Paper-Agent/blob/9bac59b633dde1856516779687260a0f562f8b9e/README.md)
- [Documentation: docs/aipe-integration.md](https://github.com/FulongLi/AIPE-IEEE-Paper-Agent/blob/9bac59b633dde1856516779687260a0f562f8b9e/docs/aipe-integration.md)

## AIPE Magnetics

Evidence-first magnetic engineering expert: unified magnetic data standard v0.2, loss and hysteresis models with per-capability verification evidence, inductor/transformer design calculations, local MCP server and standalone Codex / Claude Code plugins.

Capabilities: magnetics-record-schema, magnetics-data-import, magnetics-data-validation, magnetics-data-migration, magnetics-waveform-storage, magnetics-source-adapters, magnetics-material-lookup, magnetics-material-comparison, magnetics-core-loss-estimation, magnetics-hysteresis-evaluation, magnetics-inductor-design, magnetics-transformer-design, magnetics-waveform-informed-transformer-design, magnetics-measurement-requests, magnetics-design-validation, magnetics-engineering-report, magnetics-verification-suite, magnetics-mcp-server, magnetics-agent-plugin, magnetics-core-state-export.

Licence: `NOASSERTION`. Validation: `tested`.

- [Claude Code](https://code.claude.com/): free_proprietary; optional; interfaces: cli.
- [OpenAI Codex CLI](https://github.com/openai/codex): open_source; optional; interfaces: cli.
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk): open_source; optional; interfaces: mcp.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python, mcp.
- [PyTorch](https://pytorch.org/): open_source; optional; interfaces: python.
- Limitation: Verification evidence is recorded per capability and operating range (levels L1-L3); there is no repository-wide validated flag.
- Limitation: Model implementations are verified against analytical, independent-numerical and published references (L2); no experimental (L3) validation is bundled.
- Limitation: Material and core parameters are datasheet-derived with locators and remain review_status unreviewed until an owner review.
- Limitation: No third-party datasets are redistributed; adapters download or import on demand subject to each source licence.
- Limitation: Repository licence remains NOASSERTION pending owner decision.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/README.md)
- [Documentation: CHANGELOG.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/CHANGELOG.md)
- [Documentation: docs/architecture.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/architecture.md)
- [Documentation: docs/audit-v0.1.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/audit-v0.1.md)
- [Documentation: docs/data-standard-v0.2.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/data-standard-v0.2.md)
- [Documentation: docs/models.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/models.md)
- [Documentation: docs/verification.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/verification.md)
- [Documentation: docs/api.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/api.md)
- [Documentation: docs/mcp.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/mcp.md)
- [Documentation: docs/plugins.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/plugins.md)
- [Documentation: docs/core-integration.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/core-integration.md)
- [Documentation: docs/sources.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/sources.md)
- [Documentation: docs/demo-dab-10kw.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/demo-dab-10kw.md)
- [Documentation: docs/waveform-informed-design.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/docs/waveform-informed-design.md)
- [Documentation: LICENSING.md](https://github.com/FulongLi/AIPE-Magnetics-Database/blob/59eff8b58186b1239f00bb12685738a2da109017/LICENSING.md)

## Open Engineering Tool Catalogue

Community-curated external engineering tools with dated maintenance, licence and automation evidence.

Capabilities: external-tool-discovery, external-tool-maintenance-audit.

Licence: `NOASSERTION`. Validation: `tested`.

- [Python](https://www.python.org/): open_source; required; interfaces: cli.
- Limitation: No external solver or MCP execution validated. Catalogue inclusion does not imply AIPE support.
- [Documentation: README.md](https://github.com/FulongLi/awesome-open-source-power-electronics/blob/2ff81b28669d8c9a27a150eb2b2fd85bb70a76a5/README.md)
- [Documentation: CONTRIBUTING.md](https://github.com/FulongLi/awesome-open-source-power-electronics/blob/2ff81b28669d8c9a27a150eb2b2fd85bb70a76a5/CONTRIBUTING.md)
- [Documentation: generated/audit.md](https://github.com/FulongLi/awesome-open-source-power-electronics/blob/2ff81b28669d8c9a27a150eb2b2fd85bb70a76a5/generated/audit.md)

## AIPE Labs Presentation

Jekyll presentation and stable public URLs for Registry capabilities and Academy lessons.

Capabilities: ecosystem-presentation, academy-publication.

Licence: `CC-BY-4.0`. Validation: `tested`.

- [Jekyll](https://jekyllrb.com/): open_source; required; interfaces: cli.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Presentation validation does not validate engineering claims.
- Limitation: Deployment follows reviewed PR merges; no live deployment performed.
- Limitation: Registry initialization has a local-only baseline until upstream empty-repository permissions are resolved.
- [Documentation: README.md](https://github.com/FulongLi/Spirit-Connect-AIPE-Labs/blob/3ed4f5271b319f68b469fd054cfb94b69627cb81/README.md)
- [Documentation: docs/ecosystem-v0.1.md](https://github.com/FulongLi/Spirit-Connect-AIPE-Labs/blob/3ed4f5271b319f68b469fd054cfb94b69627cb81/docs/ecosystem-v0.1.md)

## AIPE Registry

Discover and validate canonical AIPE capabilities and publish reproducible machine-readable and Markdown indexes.

Capabilities: capability-discovery, capability-manifest-validation, deterministic-registry-publication.

Licence: `MIT`. Validation: `tested`.

- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Core and Engineering State version identifiers are recognized; Registry does not transform engineering states.
- Limitation: Staging snapshots may precede upstream merge; inspect sources/snapshots.lock.json before deployment.
- Limitation: Snapshot-only checks cannot verify repository-relative documentation existence; use --checkouts for that audit.
- Documentation staged locally (publication pending): `README.md`
- Documentation staged locally (publication pending): `CONTRIBUTING.md`

## AIPE Semiconductor Database

Canonical V3 power semiconductor records with SI curves, source rights, evidence lineage, a conservative Core candidate adapter, DAB switch loss evaluation on actual waveform stress, evidence-tiered device screening, datasheet candidate import and prioritised measurement requests.

Capabilities: semiconductor-data, semiconductor-query, semiconductor-core-candidate-export, semiconductor-loss-evaluation, semiconductor-dab-screening, semiconductor-measurement-requests, candidate-device-import.

Licence: `NOASSERTION`. Validation: `tested`.

- [MATLAB](https://www.mathworks.com/products/matlab.html): commercial; optional; interfaces: file.
- [PLECS](https://www.plexim.com/plecs): commercial; optional; interfaces: file.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: Identity/source mapping only; detailed ratings and curves stay in V3 records.
- Limitation: Manufacturer model data is not converted into measured evidence.
- Limitation: Existing code and data rights remain NOASSERTION; see LICENSING.md.
- Limitation: DAB losses derive from manufacturer PLECS tensors and datasheet points; ZVS turn-on loss is zero by assumption without Coss/Eoss evidence.
- Limitation: Candidate device records are unreviewed datasheet transcriptions and are not canonical evidence.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-Semiconductor-Database/blob/52ec17db4098e96078ac10d683aceddf999e5c94/README.md)
- [Documentation: docs/dab-loss-screening.md](https://github.com/FulongLi/AIPE-Semiconductor-Database/blob/52ec17db4098e96078ac10d683aceddf999e5c94/docs/dab-loss-screening.md)
- [Documentation: docs/core-integration.md](https://github.com/FulongLi/AIPE-Semiconductor-Database/blob/52ec17db4098e96078ac10d683aceddf999e5c94/docs/core-integration.md)
- [Documentation: docs/architecture.md](https://github.com/FulongLi/AIPE-Semiconductor-Database/blob/52ec17db4098e96078ac10d683aceddf999e5c94/docs/architecture.md)
- [Documentation: LICENSING.md](https://github.com/FulongLi/AIPE-Semiconductor-Database/blob/52ec17db4098e96078ac10d683aceddf999e5c94/LICENSING.md)
- [Documentation: data/candidates/README.md](https://github.com/FulongLi/AIPE-Semiconductor-Database/blob/52ec17db4098e96078ac10d683aceddf999e5c94/data/candidates/README.md)

## AIPE Simulation Skills

Engineering-purpose simulation, control, CAD, PCB and field-analysis skills with an open-source default and preserved optional proprietary workflows, plus the executable aipe_simulation package: ngspice qualification and batch runner, dual-active-bridge switching-circuit generator (ideal and behavioural levels) and a solver-independent waveform analysis engine (HDF5 datasets, steady-state detection, per-switch metrics).

Capabilities: averaged-control-analysis, switching-circuit-simulation, mechanical-packaging, pcb-power-stage-review, field-analysis-problem-setup, digital-control-debugging, dab-switching-circuit-generation, waveform-analysis-engine, solver-tool-qualification.

Licence: `NOASSERTION`. Validation: `tested`.

- [ANSYS](https://www.ansys.com/): commercial; optional; interfaces: scripting.
- [CalculiX](https://www.calculix.de/): open_source; optional; interfaces: cli, inp.
- [COMSOL](https://www.comsol.com/): commercial; optional; interfaces: java-api, batch.
- [Elmer FEM](https://github.com/ElmerCSC/elmerfem): open_source; optional; interfaces: cli, sif.
- [FreeCAD](https://www.freecad.org/): open_source; optional; interfaces: python, cli.
- [GetDP](https://getdp.info/): open_source; optional; interfaces: cli, pro.
- [Gmsh](https://gmsh.info/): open_source; optional; interfaces: cli, python.
- [KiCad](https://www.kicad.org/): open_source; optional; interfaces: cli, ipc, python.
- [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html): free_proprietary; optional; interfaces: batch, netlist.
- [MATLAB / Simulink](https://www.mathworks.com/products/simulink.html): commercial; optional; interfaces: matlab, batch.
- [ngspice](https://ngspice.sourceforge.io/): open_source; optional; interfaces: cli, netlist.
- [openEMS](https://www.openems.de/): open_source; optional; interfaces: python, octave.
- [PLECS](https://www.plexim.com/plecs): commercial; optional; interfaces: scripting, xml-rpc.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- [python-control](https://python-control.org/): open_source; optional; interfaces: python.
- [SIMetrix / SIMPLIS](https://www.simetrix.co.uk/): commercial; optional; interfaces: scripting, netlist.
- Limitation: Local Python numerical tests passed; ngspice solver tests (tests/test_dab_ngspice.py, marker 'solver') ran against ngspice 47 on Windows and are skipped when ngspice is absent.
- Limitation: Executed DAB simulations are Level 1 ideal and Level 2 behavioural models with datasheet-sourced parameters; no manufacturer SPICE model (Level 3) has been executed or validated.
- Limitation: FreeCAD, KiCad, FEA solvers and MCP connectors are not executed by this repository; their skills remain procedural guidance.
- Limitation: No measurements or full Engineering State round-trip adapter claimed; AIPE-Workflows maps the run outputs into Core evidence.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/README.md)
- [Documentation: docs/tool-policy.md](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/docs/tool-policy.md)
- [Documentation: docs/core-mapping.md](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/docs/core-mapping.md)
- [Documentation: skills.json](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/skills.json)
- [Documentation: docs/validation.md](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/docs/validation.md)
- [Documentation: docs/dab-models.md](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/docs/dab-models.md)
- [Documentation: pyproject.toml](https://github.com/FulongLi/AIPE-Simulation-Skills/blob/454738f06547e5ccca1087c6d33e83c67a4d6c86/pyproject.toml)

## AIPE Sketcher

AI-powered electrical schematic generation for power electronics and circuit engineering. Renders explicit Circuit IR into connectivity-checked SVG schematics with validation reports and provenance; installable as a Codex and Claude Code plugin.

Capabilities: schematic-generation, circuit-connectivity-validation.

Licence: `LicenseRef-AIPE-Sketcher-Personal-NonCommercial-0.1 AND CC0-1.0`. Validation: `tested`.

- [Claude Code](https://code.claude.com/): free_proprietary; optional; interfaces: cli, gui.
- [OpenAI Codex](https://github.com/openai/codex): open_source; optional; interfaces: cli, gui.
- [Inkscape](https://inkscape.org/): open_source; optional; interfaces: cli, gui.
- [Python](https://www.python.org/): open_source; required; interfaces: python, cli.
- Limitation: Explicit Circuit IR and complete Core validation are required separately; no device sizing or physical results are inferred.
- [Documentation: README.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/README.md)
- [Documentation: docs/README.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/docs/README.md)
- [Documentation: docs/plugins.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/docs/plugins.md)
- [Documentation: docs/cli.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/docs/cli.md)
- [Documentation: docs/engineering-state.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/docs/engineering-state.md)
- [Documentation: docs/architecture.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/docs/architecture.md)
- [Documentation: LICENSE](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/LICENSE)
- [Documentation: THIRD_PARTY_NOTICES.md](https://github.com/FulongLi/AIPE-Sketcher/blob/3e005d08d4bca7afc86366412494a3755b0b637e/THIRD_PARTY_NOTICES.md)

## AIPE Workflows

System-level engineering workflow engine executing typed, checkpointed task graphs over AIPE specialist capabilities (design agent, simulation skills, semiconductor and magnetics databases, field simulation, CAD agent), with local tool qualification, Engineering State provenance, cross-module feedback iterations, verification gates and report assembly; first benchmark is the simulation-driven 10 kW dual-active-bridge converter.

Capabilities: engineering-workflow-execution, workflow-task-graph, capability-discovery-client, environment-tool-qualification, engineering-state-provenance, verification-gate-ledger, engineering-report-assembly.

Licence: `MIT`. Validation: `tested`.

- [Elmer FEM](https://github.com/ElmerCSC/elmerfem): open_source; optional; interfaces: cli, sif.
- [FreeCAD](https://www.freecad.org/): open_source; optional; interfaces: cli, python.
- [Gmsh](https://gmsh.info/): open_source; optional; interfaces: python, cli.
- [KiCad](https://www.kicad.org/): open_source; optional; interfaces: cli.
- [ngspice](https://ngspice.sourceforge.io/): open_source; optional; interfaces: cli.
- [Python](https://www.python.org/): open_source; required; interfaces: cli, python.
- Limitation: The DAB reference run executes analytical design, ngspice Levels 1 and 2, waveform-informed magnetics, device screening and losses, SPS control baseline, cooling comparison and heat-sink screening, Gmsh/Elmer window and heat-sink FEM, and FreeCAD transformer and heat-sink geometry; PCB boards are produced by AIPE-PCB-Agent outside the task graph and CFD, manufacturer SPICE models (Level 3), measurement and hardware stages are not executed.
- Limitation: Specialist results are analytical correlations, manufacturer data or executed numerical models with stated validity ranges; none is a measured value.
- Limitation: A completed workflow run establishes software and simulation gates only; engineering review, experimental measurement and hardware qualification are separate statuses that this engine never asserts.
- Limitation: Capability discovery reads manifests as data; it does not execute connectors or install software.
- Documentation staged locally (publication pending): `README.md`
- Documentation staged locally (publication pending): `docs/architecture.md`
- Documentation staged locally (publication pending): `docs/execution-envelope.md`
- Documentation staged locally (publication pending): `docs/capability-matrix.md`
- Documentation staged locally (publication pending): `workflows/converter_dab/README.md`
- Documentation staged locally (publication pending): `examples/dab-10kw/README.md`
