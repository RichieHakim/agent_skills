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

| Partition | GPU/node | Cores/node | RAM/node | Max wall |
|---|---|---|---|---|
| `kempner` | 4× A100 40G | 64 | ~1 TB | 7d |
| `kempner_h100` | 4× H100 80G | 96 | ~1.5 TB | 3d |
| `kempner_requeue` | mixed (A100/H100/H200) | varies | varies | 7d (preemptible) |
| `kempner_interactive` | A100 MIG 3g.20gb | 64 | 1 TB | 8h |

Per-GPU caps: `kempner` ≤ 16c / 240G; `kempner_h100` ≤ 24c / 375G. No `kempner_h200` — use `kempner_requeue --constraint=h200` or FAS `gpu_h200`.

### Limits

- 16 GPUs per `kempner_*` account (shared across all users of that account)
- 1 GPU per user on `kempner_interactive`
- For sweeps: `--array=0-N%15` to keep a slot free

### SBATCH blocks

1 GPU slice = 1 GPU + 1/4 of the node cores & RAM. Scale linearly for multi-GPU.

**`kempner` — 1× A100**
```bash
#SBATCH --partition=kempner
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=249000M
#SBATCH --time=1-00:00:00
```

**`kempner_h100` — 1× H100**
```bash
#SBATCH --partition=kempner_h100
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 24
#SBATCH --mem=374000M
#SBATCH --time=1-00:00:00
```

**`kempner_requeue`** — pin GPU type with `--constraint`. Size cores/mem to hardware.
```bash
#SBATCH --partition=kempner_requeue
#SBATCH --account=kempner_rhakim_lab
#SBATCH --constraint=h200
#SBATCH --gres=gpu:1
#SBATCH -c 24
#SBATCH --mem=374000M
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
| A100 GPU | ~190 |
| H100 / H200 GPU | ~547 |

Requeue partitions bill at 50%.

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
- Kempner: [Overview](https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/kempner_cluster/overview_of_kempner_cluster.html) · [Responsible use](https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/kempner_cluster/kempner_policies_for_responsible_use.html) · [Advanced SLURM](https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/general_hpc_concepts/advanced_slurm_features.html)
