# Resource availability and data-fit checks

Checks read public README files only. No dataset was downloaded, no code executed, and no form submitted. HTTP 200 for documentation is not proof that every data file is downloadable or that reuse is licensed for the intended experiment. See resource-access-check.json for exact URLs and returned excerpts.

| Resource | What was verified | What it can support | What must not be inferred |
|---|---|---|---|
| CAR-bench repository | Public README identifies the paper, synthetic user/tool environment, external dataset hosting and API-key requirements; distinguishes the paper repository from a competition repository | Multi-turn consistency, ambiguity and capability-awareness protocols | Real driver preferences, physiological benefit or free evaluation; no benchmark run was made |
| Agentic feedback supplement | Public README lists condition videos and a qualitative codebook for 2602.15569 | Reconstructing feedback conditions and qualitative coding concepts | Open raw participant transcripts or permission to redistribute participant data |
| AIDE repository | Public README identifies the ICCV2023 dataset and multi-view driving perception context | Checking which driver/traffic labels and camera views are actually available | Continuous sessions, support-demand labels or permission to repurpose data without reviewing its access terms |
| CREMA-D | Public README describes acted audiovisual emotional utterances, Git LFS media handling and ODbL/database-contents terms | Defined speech-emotion baselines with appropriate licensing checks | Naturally synchronized road/driver data, real driver distress, or requests for emotional support |
| When2Talk testbed | Paper points to a CARLA/VR project page | A lead for reproducing passenger communication-timing tasks | Testbed/data availability has not been independently checked here; no page download was used to assert a release |
| InCarEmo | Earlier pilot read the dataset paper's scripted-scenario/annotation description | Candidate in-cabin recognition data after access/label checks | Release status, permission and real-world support preference labels remain unverified |

A separate future experiment needs a frozen task/label definition, license/access review, participant-role match and independent outcome measurements. Public recorded speech or subjective text ratings alone do not supply ground truth for whether an actual driver wants intervention.
