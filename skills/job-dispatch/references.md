# Harvard FAS RC (Cannon / Kempner) — cheat sheet

Cluster info for `rhakim`. 
Docs: 
- <https://docs.rc.fas.harvard.edu/>
- Kempner: <https://handbook.eng.kempnerinstitute.harvard.edu/>
- FAS: <https://docs.rc.fas.harvard.edu/kb/running-jobs/>, <https://docs.rc.fas.harvard.edu/kb/category/cluster-usage/>

## Accounts

| Account | Partitions | Notes |
|---|---|---|
| `kempner_rhakim_lab` | all `kempner*` | Default for GPU work |
| `kempner_bsabatini_lab` | all `kempner*` | Larger lab shares |
| `kempner_konkle_lab` | all `kempner*` | Larger lab shares |
| `kempner_ba_lab` | all `kempner*` | Larger lab shares |
| `rhakim_lab` | all FAS partitions | Only working FAS account |

Fairshare: default to `kempner_rhakim_lab`. Slowdown below ~0.7; hard to allocate below ~0.5. Check: `sshare -U`.

## Tips

- Allocation typically takes around 10-60 seconds at best, and much slower at worst. Plan to batch jobs if runtime is on the order of allocation time.

## Kempner

### Partitions

All four main GPU partitions share a **2-day max wall** and the `kempner_base` QOS.

| Partition | GPU/node | Cores/node | RAM/node | Max wall |
|---|---|---|---|---|
| `kempner` | 4× A100 40G | 64 | ~1 TB | 2d |
| `kempner_h100` | 4× H100 80G | 96 | ~1.5 TB | 2d |
| `kempner_h200` | 4× H200 141G | 64 | ~1.5 TB | 2d |
| `kempner_rtx` | 8× RTX PRO 6000 96G | 128 | ~1.5 TB | 2d |
| `kempner_requeue` | mixed (A100/H100/H200/RTX) | varies | varies | 2d (preemptible) |
| `kempner_interactive` | A100 MIG 3g.20gb (8 slices/node) | 64 | ~1 TB | 8h |

GPU picking: **A100** for small/proto & max software compatibility; **H100/H200** for large-scale training/inference (FP8, NVLink); **H200** for the largest/long-context models (141 GB, highest bandwidth); **RTX** for FP4 / rendering / RL (8/node, PCIe not NVLink — weaker multi-GPU sharding). Precision: FP8 on H100/H200/RTX; FP4 on RTX only.

Relative single-GPU throughput (Kempner's BF16-training benchmark, ~1B transformer): **A100 ≈ 1× · RTX ≈ 1.4× · H100 ≈ 2.4× · H200 ≈ 2.6×**. Memory bandwidth: H200 ~40% > H100, ~3× A100/RTX. Cross against the billing table below for perf-per-fairshare — RTX is the cheapest *and* ~1.4× an A100. Full benchmarks: "Choosing a GPU partition" (Docs).

Per-GPU share — request this much cores/RAM for *each* GPU you request: `kempner` 16c / 240G · `kempner_h100` 24c / 360G · `kempner_h200` 16c / 360G · `kempner_rtx` 16c / 180G. These are just the node's cores and RAM split across its GPUs (cores = cores÷GPUs exactly; RAM ≈ node RAM÷GPUs, rounded down for OS overhead), so *k* GPUs → *k*× these values = *k*/(GPUs-per-node) of the node. The scheduler doesn't enforce this (only the 16-GPU/user QOS cap is hard), but overshooting your share strands the node's other GPUs — they can't be allocated to anyone else.

### Limits

- **16 GPUs per user**, aggregated across `kempner` + `kempner_h100` + `kempner_h200` + `kempner_rtx` (QOS `kempner_base`, `MaxTRESPU=gres/gpu=16`).
- **96 GPUs per account** (`GrpTRES`; `kempner_undergrads` = 4).
- 1 GPU per user on `kempner_interactive`.
- To exceed caps: use `kempner_requeue` (preemptible), shorten runtimes, or request a reservation via Cluster Governance. Monopolizing gets jobs killed without notice and fairshare cut.
- For sweeps: `--array=0-N%15` to keep one slot free.

### `#SBATCH` header templates (one per partition)

Copy or adapt the block below matching the GPU you want into your worker `.sh` header. Each block requests **one GPU's share** of the node (1/4 node on A100/H100/H200, 1/8 on RTX — 8 GPUs/node); for *N* GPUs, set `--gres=gpu:N` and scale `-c`/`--mem` by *N*. `G` vs `M` suffix both fine; stay at/under the per-GPU share above.

**`kempner` — 1× A100**
```bash
#SBATCH --partition=kempner
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=240G
#SBATCH --time=1-00:00:00
```

**`kempner_h100` — 1× H100**
```bash
#SBATCH --partition=kempner_h100
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 24
#SBATCH --mem=360G
#SBATCH --time=1-00:00:00
```

**`kempner_h200` — 1× H200** (141 GB VRAM, highest bandwidth)
```bash
#SBATCH --partition=kempner_h200
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=360G
#SBATCH --time=1-00:00:00
```

**`kempner_rtx` — 1× RTX PRO 6000 Blackwell** (96 GB, 8/node, PCIe, FP4-capable). Now the **cheapest GPU** for fairshare (see below).
```bash
#SBATCH --partition=kempner_rtx
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=180G
#SBATCH --time=1-00:00:00
```

**`kempner_requeue`** — preemptible; pin GPU type with `--constraint` (features: `a100`, `h100`, `h200`, `rtx6000pro`, `a100-mig`). Size cores/mem to the chosen hardware.
```bash
#SBATCH --partition=kempner_requeue
#SBATCH --account=kempner_rhakim_lab
#SBATCH --constraint=h200
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=360G
#SBATCH --time=1-00:00:00
#SBATCH --requeue
```

## FAS / Cannon

Account: `rhakim_lab`. No hard per-user CPU/memory/job caps on production partitions.

### Partitions

| Partition | Cores/node | RAM/node | GPU/node | Max wall | Notes |
|---|---|---|---|---|---|
| `sapphire` | 112 | ~1 TB | — | 3d | Preferred CPU. ≤64c for fast scheduling. |
| `shared` | 48 | ~184 GB | — | 3d | General CPU |
| `serial_requeue` | mixed | varies | mixed | 3d | Preemptible, 50% fairshare cost |
| `gpu` | 64 | ~990 GB | 4× A100-80GB | 3d | sinfo: 1031177 MB/node. No enforced per-GPU split. |
| `gpu_h200` | 112 | ~1 TB | 4× H200 | 3d | sinfo: 1031252 MB/node. |
| `gpu_requeue` | mixed | varies | mixed | 3d | Preemptible GPU, 50% cost |
| `bigmem` | 112 | ~2 TB | — | 3d | Only when >1 TB RAM needed |
| `intermediate` | 112 | ~1 TB | — | 14d | Must request >3d walltime |
| `unrestricted` | 48 | ~184 GB | — | 365d | No uptime guarantee |
| `test` / `gpu_test` | varies | varies | varies | 12h | 5 / 2 jobs, 112 / 64 CPUs max |

### SBATCH block

**`sapphire` — CPU.** Full node `-c 112 --mem=990G` rarely schedules; stay ≤64c.
```bash
#SBATCH --partition=sapphire
#SBATCH --account=rhakim_lab
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH --time=0-12:00:00
```

**`gpu` — 1× A100-80GB.** Unlike Kempner, FAS docs do NOT enforce a per-GPU memory split — request what the app actually needs, not 1/Ngpu of the node. Check actual peak with `seff <jobid>`
after a run.
```bash
#SBATCH --partition=gpu
#SBATCH --account=rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=120G
#SBATCH --time=0-04:00:00
```

## Fairshare & billing

`f = 2^(-EffectiveUsage/NormShares)`. 3-day half-life. Check: `sshare -U`. Score 1.0 = unused (top priority), 0.5 = fair share, <0.5 = overusing (longer waits, never blocked).

| Resource | Billing weight |
|---|---|
| Cascade Lake CPU | 1.0 (baseline) |
| Sapphire Rapids CPU | 0.6 |
| A100 GPU (`kempner`) | 209 / GPU |
| H100 GPU (`kempner_h100`) | 547 / GPU |
| H200 GPU (`kempner_h200`) | 547 / GPU |
| RTX6000 GPU (`kempner_rtx`) | 21 / GPU — cheapest |

Requeue partitions bill at 50%.

**Total billing at the per-GPU share** (1 GPU + its cores/RAM): `kempner_rtx` ≈ **68**, `kempner` (A100) ≈ 245, `kempner_h200` ≈ 566, `kempner_h100` ≈ 575. RTX is by far the cheapest — its low GPU weight (21) dominates and memory is cheap. Same 4c/64G request: RTX bills ~35 vs H100 ~551 (≈16×). Prefer `kempner_rtx` for fairshare when the RTX PRO 6000 fits the job.

## General limits

| Limit | Value |
|---|---|
| Jobs per account | 10,100 (recommend ≤1,000 at once) |
| Array max index | 10,000 |
| Login nodes | 1 core, 4 GB (cgroup-killed) |
| Min job runtime | 10 min |
| sbatch rate | ≥0.5s between calls |

`scancel -n <prefix>` cancels a named sweep.

## Docs

- FASRC: [Running Jobs](https://docs.rc.fas.harvard.edu/kb/running-jobs/) · [Fairshare](https://docs.rc.fas.harvard.edu/kb/fairshare/) · [Kempner partitions](https://docs.rc.fas.harvard.edu/kb/kempner-partitions/) · [GPU computing](https://docs.rc.fas.harvard.edu/kb/gpgpu-computing-on-the-cluster/)
- Kempner: [Overview](https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/kempner_cluster/overview_of_kempner_cluster.html) · [Responsible use](https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/kempner_cluster/kempner_policies_for_responsible_use.html) · [Advanced SLURM](https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/general_hpc_concepts/advanced_slurm_features.html) · [Choosing a GPU partition](https://handbook.eng.kempnerinstitute.harvard.edu/technical_blog/choosing_gpu_partition.html) (benchmarks + workload guide)
