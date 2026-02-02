---
name: coding_style
description: Defines coding philosophy, conventions, and expectations for LLM-generated code to ensure clarity, maintainability, and alignment with project workflows.
---

# Coding Style Guide

**Purpose**  
This document defines the coding philosophy, conventions, and expectations for all code written by an LLM in this project. Its goal is to make the agent’s output maximally clear, maintainable, reproducible, and aligned with the workflows, libraries, and scientific practices used throughout the codebase. The rules below describe how to name variables, structure files, write docstrings, choose libraries, handle imports, design abstractions, write numerical code, and avoid common LLM pitfalls.

---

## 1. General

### 1.1 The big 4 principles (based on forrestchang/andrej-karpathy-skills)

1. **Think before coding.** State your assumptions and uncertanaties explicitly. Provide trade-off decisions to the user.

2. **Simplicity first.** No abstractions for single-use code; no extra "flexibility" or contingency handling that wasn't requested. Ask yourself if a senior engineer say "this is overcomplicated"; if yes, simplify.

3. **Surgical edits** Touch only what you must. Clean up only your own mess. _Mention_ issues you see. If you create orphans or externalities, you can fix or mention them. Every changed line should trace directly to the user's request.

4. **Goal-Driven Execution** When you are ready to implement, use this general strategy: define success criteria, then loop until verified.

Transform tasks into verifiable goals:
- User: "Add validation" → Agent: Write tests for invalid inputs, then make them pass
- User: "Fix the bug" → Write a test that reproduces it, then make it pass
- User: "Refactor X" → Ensure tests pass before and after

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

### 1.2 Philosophy

- Consider multiple levels of abstraction. Zoom out for context and organization, and zoom in for algorithms and details.
- Be more than just a code bot; be a collaborator. Fluidly transition between roles like senior advisor, clever PhD, project manager, software dev, and various engineering roles.
- Prioritize clarity. Expect humans to maintain the code; make it easy for them.
- Prioritize reproducibility. Inputs and outputs should be narrowly typed. "Explicit is better than implicit" is the law.
- Opinions and plans should precede organization, not the other way around. If organizational complexity is emerges without an explicit plan, then it should at least be described.
- Simple and flat is easy to debug. Clever and hierarchical is hard to debug. Debugging is inevitable.
- How did you get here? If you find yourself handling contingencies, fallbacks, and input sanitization, reconsider organization at a higher level of abstraction.
- This is the real-world, and is out of your training distribution. There might not be an ideal solution. You might not have sufficient information. You were trained to 'one-shot' solutions; here, it is wiser to make careful incremental progress over multiple steps.

### 1.3 Tips

- Document the intent and purpose of code blocks, functions, classes, and scripts within docstrings and inline comments.
- Remind yourself of the big picture and overall goals often. This will help keep work organized and directed.
- Keep users informed: print meaningful progress messages, discovered resources, and changes in workflow.
- Think about downstream applications and purpose. Be more than just a code bot; be a collaborator. You have a broader knowledge base than the user; inform them about what is known, what tools exist, and how others have solved problems.
- Avoid sanitization! Form opinions and expectations about data, and assert that the data conform to your specifications. Duck-typing, input variable santizing, and trying to handle contingencies results in _silent errors_ and unexpected outputs. Try/except blocks are generally evil. Err towards being too explicit, too typed, and too declarative.
- Avoid fallbacks! If a function call fails, it is better to let it fail than to try and handle it in some way. This is especially true for library calls. If you don't know what to do, ask the user.
- Ask questions. You have incomplete knowledge. If you find yourself uncertain, pause, think, and ask for clarity.

---

## 2. Libraries

- Someone else has probably solved your problem already. Use third-party libraries or repos whenever possible.
- Libraries are great at low level clever algorithms (i.e., numpy), and also for structuring workflows (sklearn models all have `.fit`, `.transform` methods; darts models all use `series`, `past_covariates`, `future_covariates` input args; torch uses `(B, C, H, W)` for indexing all images).
- Search for libraries, assess their quality, and either add them as a dependency or copy and reference their underlying code. Look for small and new repos as well. Active repo/codebase maintenance is good, well-reputed organizations/people are good, documentation is good. Sometimes, we can't be picky and just need to use what exists.

---

## 3. Variable Names

### 3.1 Global Variables
- Use long descriptive names (i.e., `kwargs_linearRegression_fast`, `accuracy_batchMean_covarianceAcrossLayers`).
- Function and method names should be descriptive verbs (`prepare_params`, `set_device`, `generate_latents`).
- Names should be hierarchical. The type of object should come first, then adjective descriptors.  
  Example: `filepath_model_save` (preferred over `model_save_filepath`).

### 3.2 Function Arguments
- Descriptive names are good. Single letter names are generally bad unless it is obvious what its function is.  
  Handing off a long variable name to a shorter one (so long as it doesn't duplicate it in memory) is good for when there is complicated math.
- Function calls should use explicit keywords for args, even when they are not required.  
  Example: `myfunc(x=3, y=5, z=8)` instead of `myfunc(3, 4, z=8)`.

---

## 4. Common Tasks

### 4.1 Saving and Loading
- Use `pathlib.Path` for most path creation and navigation operations (avoid `os.path`).
- Path variables should generally be maintained as string objects, not `pathlib.Path` objects.  
  Example:  
  `filepath_model = str(Path(dir_model) / (filename_model + ".pth"))`
- Use `filepath_...` for files and `dir_...` for directories.
- For collections (lists, dicts, etc.) of paths, use plurals.  
  Example: `filepaths_models`, `dirs_models`, etc.

### 4.2 Data Paths
- Generally, do not assume any structure to where data paths can be found.
- For user-level scripts, ingest filepaths and directory paths for saving. For .sh and dispatch-level scripts, you may hardcode paths.

---

## 5. Documentation

### 5.1 Docstrings
- Use RST/Google-style with multi-line nested descriptions for Args and Returns.
- Do not write in what the default is if it can be surmised from the function header and/or typing.
- Intuitive and detailed natural language descriptions are critical.
- Even small utilities must contain a docstring.
- Return objects must be named and described.
- Include examples when helpful.
- Compatibility with ReadTheDocs is preferred.

#### Examples

```python
def deep_update_dict(
    dictionary: dict, 
    key: List[str], 
    val: Any, 
    in_place: bool = False
) -> Union[dict, None]:
    """
    Updates a nested dictionary with a new value.

    Args:
        dictionary (dict): 
            The original dictionary to update.
        key (List[str]): 
            List of keys representing the hierarchical path to the nested value
            to update. Each element should be a string that represents a level
            in the hierarchy. For example, to change a value in the dictionary
            `params` at key 'dataloader_kwargs' and subkey 'prefetch_factor', you would 
            pass `['dataloader_kwargs', 'prefetch_factor']`.
        val (Any): 
            The new value to set in the dictionary.
        in_place (bool): 
            * ``True``: the original dictionary will be updated in-place and no
              value will be returned. 
            * ``False``, a new dictionary will be created and returned.

    Returns:
        (Union[dict, None]): 
            updated_dict (dict): 
                The updated dictionary. Only returned if ``in_place`` is ``False``.
                
    Example:
        .. highlight:: python
        .. code-block:: python

            original_dict = {"level1": {"level2": "old value"}}
            updated_dict = deep_update_dict(original_dict, ["level1", "level2"], "new value", in_place=False)
    """
    ...
```

```python
def phase_correlation(
    im_template: Union[np.ndarray, torch.Tensor],
    im_moving: Union[np.ndarray, torch.Tensor],
    mask_fft: Optional[Union[np.ndarray, torch.Tensor]] = None,
    return_filtered_images: bool = False,
    eps: float = 1e-8,
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Perform phase correlation on two images. Calculation performed along the
    last two axes of the input arrays (-2, -1) corresponding to the (height,
    width) of the images.

    Args:
        im_template (np.ndarray): 
            The template image(s). Shape: (..., height, width). Can be any
            number of dimensions; last two dimensions must be height and width.
        im_moving (np.ndarray): 
            The moving image. Shape: (..., height, width). Leading dimensions
            must broadcast with the template image.
        mask_fft (Optional[np.ndarray]): 
            2D array mask for the FFT. If ``None``, no mask is used.
        return_filtered_images (bool): 
            If set to ``True``, returns filtered images.
        eps (float):
            Epsilon to prevent division by zero.
    
    Returns:
        (Tuple[np.ndarray, np.ndarray, np.ndarray]): tuple containing:
            cc (np.ndarray): 
                The phase correlation coefficient.
            fft_template (np.ndarray): 
                The filtered template image. Only returned if
                return_filtered_images is ``True``.
            fft_moving (np.ndarray): 
                The filtered moving image. Only returned if
                return_filtered_images is ``True``.
    """
    ...
```

```python
def compose_transform_matrices(
    matrix_AB: np.ndarray, 
    matrix_BC: np.ndarray,
) -> np.ndarray:
    """
    Composes two transformation matrices to create a transformation from one
    image to another. 
    RH 2023

    Args:
        matrix_AB (np.ndarray): 
            A transformation matrix from image A to image B. Shape (2,3) or (3,3).
        matrix_BC (np.ndarray): 
            A transformation matrix from image B to image C. Shape (2,3) or (3,3).

    Returns:
        (np.ndarray): 
            matrix_AC (np.ndarray):
                A composed transformation matrix.

    Raises:
        AssertionError: 
            If input shapes are invalid.
    """
    ...
```

### 5.2 Comments
- Add inline comments describing variable properties (tensor shapes, indexing changes, python types).
- Add step/code-block headers (`## Section`) every 3–10 lines to describe intent.
- Avoid non-keyboard characters unless necessary.
- Communicate intent clearly using analogies, concrete examples, and explicit detail.
- References to papers, equations, and algorithms are encouraged.
- Latex formatting is acceptable when needed.

---

## 6. Importing
- Generally import top-level libraries and call functions via namespace.  
  Example: `import torch`, then `torch.nn.functional.cosine_similarity(...)`.
- Exceptions include `from tqdm.auto import tqdm`, `from pathlib import Path`, etc.
- Group imports by category and separate by blank lines:

```python
from typing import List  ## typing

import os
import sys
from pathlib import Path  ## built-ins

import numpy as np
import torch  ## third-party

import basic_neural_processing_modules as bnpm
import vqt  ## personal

from .model_def import build_model  ## working repo/library
```

---

## 7. Abstraction
- Hierarchical organization is generally good; unnecessary obscurity is bad.
- Keep hierarchy flat.
- Abstract functions only when they remove duplication or prevent holding large global variables.
- Prefer multi-use functions over many decoupled functions.
- Avoid clever constructs: returning functions, custom decorators, special class behaviors.

Example of a pointless abstraction that should be avoided without good reason:
```python
def _needs_residual_blend(config) -> bool:
    return config.get('residual_profile') is not None

def apply_residual_config(dino, config):
    if not _needs_residual_blend(config):
        return dino
    ...
```
Instead just do:
```python
def apply_residual_config(dino, config):
    if not config.get('residual_profile') is not None:
        return dino
    ...
```

---

## 8. Numerical Computing
- Write functions in a jit-friendly manner when feasible (numba, torch.jit.script, jax jit). Some sharp bits for jit-able functions: avoid in-place operations; use `if: raise(...)`, not `assert`; keep shapes rigid. For more details: https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html
- Preferred stylistic conventions:  
  - Use `[None, ...]`, not `.unsqueeze(0)`  
  - Avoid `.squeeze()`  
  - Prefer `.T` to `.t()`  
  - If using `matmul(a, b)` over `a @ b`, explain why. If using `reshape` over `view`, explain why.
  - Use `torch.as_tensor(...)` for ingestion
- Comment on broadcasting and shape changes
- Vectorization > for-loops.
- Walrus operator is good for comprehensions: `[(x := h) + x**2 for h in hs]`
- Prefer dictionaries over pandas unless we can benefit from pandas-specific methods.
- Dataclasses and configs are good.
- Prefer `np.memmap` and `zarr` for large arrays.
- Sparse arrays are good. Scatter-add is good. vmap is good. einsum is good.
- Functions with randomness should be provided with seeds or at least comment/docstring line noting the randomness.

---

## 9. Other
- Use Black-style formatting. For more details: https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html
- Fail loudly. Validate inputs early using assertions and clear error messages.
- Avoid accepting wide varieties of inputs and reformatting them to work; be opinionated in inputs and outputs.
- `pydantic` can be useful on occasion.
- Avoid multiple return types unless necessary.
- Avoid global state and environment variables.
- Tests are good. Prefer `pytest`. Basic tests should be fore correctness, secondary tests should look at edge cases (weird shapes, types, NaNs, strange values).
- If you have agentic access to a coding environment, testing code is good.
- Don't use `None` directly in `if` statements; always convert to a boolean (`if x is None`).

---

## 10. Known Difficulties (LLM Failure Modes)
- Context is limited. Know your limitations and self-prompt to retain important info.
- You want to be generally applicable. I want to be specific. You have a tendency to be vague. I have a tendency to be narrow-minded. Bridge this gap by identifying the underlying goal.
- Do not invent or change config fields, directories, functions, call signatures, comments (even "TODO"s), or infrastructure without asking the user first and then prominently noting it.
- If you provide or edit some piece of code, but then you see it later with changes applied, assume that those changes were made by a user, are very important, and shouldn't be reverted back.
- Hallucination is still a problem. Don't make assumptions on the user's behalf without checking with them first.

### 10.1 Quotes from Andrej Karpathy

> "The models make wrong assumptions on your behalf and just run along with them without checking. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."

> "They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code... implement a bloated construction over 1000 lines when 100 would do."

> "They still sometimes change/remove comments and code they don't sufficiently understand as side effects, even if orthogonal to the task."

---

## 11. GPU Tensor Handling

Rules for working with PyTorch tensors.

1. **Delete large intermediate tensors explicitly**
   ```python
   del large_tensor
   torch.cuda.empty_cache()
   ```

2. **Use configurable device strings**
   ```python
   DEVICE = config.device  # "cuda:0" or "cpu"
   tensor = tensor.to(DEVICE)
   ```

3. **Prefer numpy format for portability** when saving analysis results (`.npy`/`.npz`).