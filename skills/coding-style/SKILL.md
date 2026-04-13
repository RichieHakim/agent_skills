---
name: coding-style
description: Coding philosophy, conventions, and expectations for Python code.
---

# Coding Style

## Philosophy

1. **Think first.** State assumptions and uncertainties. Present trade-offs before implementing.
2. **Simplicity first.** No abstractions for single-use code. No unrequested contingency handling. If a senior engineer would say "overcomplicated" — simplify.
3. **Surgical edits.** Touch only what you must. Mention issues elsewhere; fix only the mess.
4. **Verify your work.** Transform tasks into verifiable goals: write a test, make it pass. For multi-step tasks, state a brief plan with checks.

Be a collaborator, not a code bot. You have broad knowledge — inform the user about tools, approaches, and prior work they may not know. If you see a better approach than what was asked for, say so — a one-line aside is enough. Consider multiple levels of abstraction: zoom out for organization, zoom in for algorithms.

This is the real world and often out of your training distribution. Prefer careful incremental progress over one-shot attempts. When uncertain, ask.

## Naming

- **Variables:** long, hierarchical, type-first. `kwargs_linearRegression_fast`, `accuracy_batchMean_covarianceAcrossLayers`.
- **Functions:** descriptive verbs. `prepare_params`, `generate_latents`.
- **Paths:** `filepath_*` for files, `dir_*` for directories, plurals for collections (`filepaths_models`).
- **Args:** descriptive (not single letters unless math context). Always use explicit keywords: `func(x=x, y=y)`.
- Use `pathlib.Path` for composition, `str` for storage: `filepath_model = str(Path(dir_model) / (name + ".pth"))`.

## Imports

Import top-level libraries, call via namespace (`torch.nn.functional.cosine_similarity(...)`). Exceptions: `from tqdm.auto import tqdm`, `from pathlib import Path`.

Group by category with blank-line separators:

```python
from typing import List  ## typing

import os
import sys
from pathlib import Path  ## built-ins

import numpy as np
import torch  ## third-party

import basic_neural_processing_modules as bnpm  ## personal

from .model_def import build_model  ## local
```

## Documentation

**Docstrings:** RST/Google-style, nested descriptions for Args and Returns. Don't restate defaults visible in the signature. Even small utilities need docstrings. Document `Raises:` for non-obvious exceptions.

```python
def phase_correlation(
    im_template: Union[np.ndarray, torch.Tensor],
    im_moving: Union[np.ndarray, torch.Tensor],
    mask_fft: Optional[Union[np.ndarray, torch.Tensor]] = None,
    eps: float = 1e-8,
) -> Tuple[np.ndarray, ...]:
    """
    Perform phase correlation on two images along last two axes (height, width).

    Args:
        im_template (np.ndarray):
            Template image(s). Shape: (..., height, width).
        im_moving (np.ndarray):
            Moving image. Must broadcast with template.
        mask_fft (Optional[np.ndarray]):
            2D FFT mask. ``None`` means no masking.
        eps (float):
            Prevents division by zero.

    Returns:
        (Tuple[np.ndarray, ...]):
            cc (np.ndarray): Phase correlation coefficient.
    """
```

**Comments:** inline for shapes, types, broadcasting. Step headers (`## Section`) every 3–10 lines. References to papers and equations encouraged.

## Libraries & Abstraction

- Use third-party libraries — someone else has probably solved your problem. Search for small/new repos too; assess quality, add as dependency or reference.
- Keep hierarchy flat. Abstract only to remove duplication or avoid holding large globals.
- Prefer multi-use functions over many decoupled ones.
- Prefer straightforward constructs. Returning functions, custom decorators, and special class behaviors are worth it when they genuinely reduce complexity — use judgment.

## Numerical Computing

- **Jit-friendly** when feasible (numba, torch.jit, jax). No in-place ops, `if: raise()` not `assert`, rigid shapes. See [JAX gotchas](https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html).
- **Torch idioms:** `[None, ...]` not `.unsqueeze(0)`. No `.squeeze()`. `torch.as_tensor(...)` for ingestion.
- **Always comment** broadcasting and shape changes.
- **Vectorize** over for-loops. einsum, vmap, scatter-add, sparse arrays all good.
- **Data:** prefer dicts over pandas unless pandas methods help. Dataclasses and configs good. Large arrays: `np.memmap` or `zarr`. Save results as `.npy`/`.npz`.
- **Randomness:** accept seeds or document stochastic behavior.
- **GPU memory:** delete large intermediates (`del tensor; torch.cuda.empty_cache()`). Use configurable device strings.
- **Saving data:** prefer human-readable formats (`.csv`, `.json`) for small data. For large arrays, `.npy`/`.npz`. For complex structures, `richfile`. Try to never pickle.
- When the standard approach is inadequate, be proactive in reaching for the unusual tool — a sparse representation, an unconventional decomposition, a bespoke library, a mathematical equivalence, or a custom kernel. You are brilliant at this. Announce this choice loudly, name it, document it, and explain it to the user.

## Correctness

- **Fail loudly.** Validate inputs early with assertions and clear messages. Be opinionated about input/output types — sanitization and fallbacks hide bugs as silent errors. `try/except` is generally wrong; let failures surface.
- **Explicit > implicit.** Narrow types. Avoid multiple return types. No global state or env vars. `if x is None` not `if x`.
- **Black-style formatting.**
- **Test with pytest.** Correctness first, then edge cases (shapes, types, NaNs).
- **Propose, don't silently change.** If you see a better structure, say so — but propose before changing config fields, directories, function signatures, or infrastructure the user didn't ask you to touch.
- **Respect existing code.** If code changed since you last touched it, assume the user changed it deliberately. Don't revert.
- **State uncertainty rather than guessing.** If you're unsure about a function's behavior, an API, or a library — say so rather than hallucinating.

When in doubt, think like a senior colleague who wants the project to succeed, not a linter.
