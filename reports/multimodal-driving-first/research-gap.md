# Research gap report

all:"autonomous driving" AND (all:"multimodal" OR all:"vision-language") AND all:"reasoning"

Evidence: retrieved arXiv metadata and abstracts. All gap/novelty claims are tentative.

No experiments have been run. Dataset and resource recommendations are unverified.

## Workflow status

Paused for explicit human approval before experiment planning. No experiment execution is implemented. State and decisions persist in state.sqlite.

## Model usage and estimated cost

Model: gpt-4.1-mini; input tokens: 4381; output tokens: 1059; estimated cost: $0.003447; request budget: $0.10.

Assumed USD/1M tokens: input 0.40, output 1.60; confirm provider billing.

## Potential gap: How can vision-language-action models be adapted to efficiently generalize across diverse autonomous driving vehicle configurations and novel unseen driving scenarios without extensive retraining?

Evidence IDs: 2511.19912v1

The paper reports strong generalization but does not fully address adaptation across diverse vehicle setups and unseen scenarios beyond their consolidated datasets and benchmarks.

## Potential gap: What is the impact of 3D spatial reasoning and counterfactual scenario generation on improving the decision-making robustness of autonomous driving vision-language models compared to traditional 2D question-answering approaches?

Evidence IDs: 2504.04348v2

Although 3D understanding and counterfactual reasoning are proposed and shown beneficial, comprehensive quantitative comparisons specifically isolating these factors versus 2D QA methods remain limited.

## Potential gap: How do different Chain-of-Thought (CoT) reasoning implementations and progressive multimodal reasoning methods compare in terms of improving numerical reasoning accuracy and causal reasoning robustness in real-time autonomous driving applications?

Evidence IDs: 2412.15208v2, 2511.22532v1, 2602.21952v1

Different CoT approaches are explored (explicit, implicit, progressive), but head-to-head comparisons of their efficiency, inference speed, and reasoning accuracy under real-time constraints are lacking.

## Hypothesis 1: Introducing progressive multimodal Chain-of-Thought reasoning with aligned multimodal training data and reinforcement fine-tuning significantly improves the numerical and causal reasoning accuracy of vision-language models in autonomous driving compared to static textual CoT methods.

Evidence IDs: 2602.21952v1, 2511.22532v1

Speculation: Progressive multimodal reasoning approximates human-like thinking by bridging semantic and physical spaces, potentially outperforming static text-only CoT approaches in reasoning tasks.

Dataset: nuScenes, Bench2Drive; baseline: Textual Chain-of-Thought based VLMs (e.g., CoT4AD); metric: Numerical reasoning accuracy, causal reasoning accuracy, open-loop and closed-loop driving task performance

Falsifiable test: Evaluate VLMs on benchmarks like nuScenes Q&A and Bench2Drive with both static textual CoT and progressive multimodal CoT models

Provisional compute estimate: Pilot: small frozen backbone with 12-16GB VRAM, ~100 GPU-hours single seed for fine-tuning and evaluation; Full: end-to-end finetuning with ~80GB VRAM GPUs, ~1000 GPU-hours across 3 seeds; Assumes multi-modal input preprocessing and RL fine-tuning steps.

## Hypothesis 2: A lightweight multi-frame vision-language model requiring at least 10x less memory and FLOPs while maintaining or improving language-based reasoning performance can enable efficient real-time autonomous driving question answering without sacrificing interpretability.

Evidence IDs: 2403.19838v2

Speculation: Efficient architectures with multi-frame inputs can reduce computational demand and enable deployment on resource-constrained autonomous vehicles.

Dataset: DriveLM dataset; baseline: Existing large LLM-based VLMs for autonomous driving question answering; metric: CIDEr, ROUGE-L, inference speed, memory usage

Falsifiable test: Compare model memory usage, FLOPs, inference time, and language-based QA metrics on DriveLM with multi-frame lightweight model vs. large model baselines

Provisional compute estimate: Pilot: small frozen vision encoder + lightweight LLM head, 8-12GB VRAM, ~20 GPU-hours single seed; Full: fine-tuning with 40GB VRAM GPU, ~200 GPU-hours across 3 seeds; Assumes multi-frame input batching and low-latency inference.

## Hypothesis 3: Vision-language-action models leveraging explicit multi-stage structured reasoning with task-specific reward models and reinforcement learning fine-tuning outperform large general-purpose LLMs (e.g., GPT-4o) in behavior reasoning and decision consistency under complex or corrupted driving conditions.

Evidence IDs: 2505.20665v2

Speculation: Structured reasoning over perception, prediction, planning, and behavior with fine-grained rewards better captures the complexities of autonomous driving than monolithic large LLMs.

Dataset: Public autonomous driving benchmarks with complex scenarios (e.g., DriveLM Q&A benchmark); baseline: ChatGPT/GPT-4o or general vision-language models without structured reinforcement signal fine-tuning; metric: Behavior reasoning accuracy, stage-wise reasoning consistency, robustness under corrupted inputs

Falsifiable test: Evaluate cross-task reasoning VLM against GPT-4o and other baselines on benchmark datasets under normal and corrupted scenario conditions.

Provisional compute estimate: Pilot: frozen vision backbone and language model head with ~16GB VRAM, ~50 GPU-hours single seed for RL fine-tuning and evaluation; Full: end-to-end tuning with ~80GB VRAM GPUs, ~800 GPU-hours across 3 seeds; Assumes availability of task-specific reward models and RL loop.

## Retrieved references

- [2403.19838v2] Multi-Frame, Lightweight & Efficient Vision-Language Models for Question Answering in Autonomous Driving — Akshay Gopalkrishnan, Ross Greer, Mohan Trivedi (2024-03-28T21:18:33Z). https://arxiv.org/abs/2403.19838v2

Vision-Language Models (VLMs) and Multi-Modal Language models (MMLMs) have become prominent in autonomous driving research, as these models can provide interpretable textual reasoning and responses for end-to-end autonomous driving safety tasks using traffic scene images and other data modalities. However, current approaches to these systems use expensive large language model (LLM) backbones and image encoders, making such systems unsuitable for real-time autonomous driving systems where tight memory constraints exist and fast inference time is necessary. To address these previous issues, we develop EM-VLM4AD, an efficient, lightweight, multi-frame vision language model which performs Visual Question Answering for autonomous driving. In comparison to previous approaches, EM-VLM4AD requires at least 10 times less memory and floating point operations, while also achieving higher CIDEr and ROUGE-L scores than the existing baseline on the DriveLM dataset. EM-VLM4AD also exhibits the ability to extract relevant information from traffic views related to prompts and can answer questions for various autonomous driving subtasks. We release our code to train and evaluate our model at https://github.com/akshaygopalkr/EM-VLM4AD.

- [2412.15208v2] OpenEMMA: Open-Source Multimodal Model for End-to-End Autonomous Driving — Shuo Xing, Chengyuan Qian, Yuping Wang, Hongyuan Hua, Kexin Tian, Yang Zhou, Zhengzhong Tu (2024-12-19T18:59:40Z). https://arxiv.org/abs/2412.15208v2

Since the advent of Multimodal Large Language Models (MLLMs), they have made a significant impact across a wide range of real-world applications, particularly in Autonomous Driving (AD). Their ability to process complex visual data and reason about intricate driving scenarios has paved the way for a new paradigm in end-to-end AD systems. However, the progress of developing end-to-end models for AD has been slow, as existing fine-tuning methods demand substantial resources, including extensive computational power, large-scale datasets, and significant funding. Drawing inspiration from recent advancements in inference computing, we propose OpenEMMA, an open-source end-to-end framework based on MLLMs. By incorporating the Chain-of-Thought reasoning process, OpenEMMA achieves significant improvements compared to the baseline when leveraging a diverse range of MLLMs. Furthermore, OpenEMMA demonstrates effectiveness, generalizability, and robustness across a variety of challenging driving scenarios, offering a more efficient and effective approach to autonomous driving. We release all the codes in https://github.com/taco-group/OpenEMMA.

- [2504.04348v2] OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning — Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, Jose M. Alvarez (2025-04-06T03:54:21Z). https://arxiv.org/abs/2504.04348v2

The advances in vision-language models (VLMs) have led to a growing interest in autonomous driving to leverage their strong reasoning capabilities. However, extending these capabilities from 2D to full 3D understanding is crucial for real-world applications. To address this challenge, we propose OmniDrive, a holistic vision-language dataset that aligns agent models with 3D driving tasks through counterfactual reasoning. This approach enhances decision-making by evaluating potential scenarios and their outcomes, similar to human drivers considering alternative actions. Our counterfactual-based synthetic data annotation process generates large-scale, high-quality datasets, providing denser supervision signals that bridge planning trajectories and language-based reasoning. Futher, we explore two advanced OmniDrive-Agent frameworks, namely Omni-L and Omni-Q, to assess the importance of vision-language alignment versus 3D perception, revealing critical insights into designing effective LLM-agents. Significant improvements on the DriveLM Q\&A benchmark and nuScenes open-loop planning demonstrate the effectiveness of our dataset and methods.

- [2505.20665v2] DriveRX: A Vision-Language Reasoning Model for Cross-Task Autonomous Driving — Muxi Diao, Lele Yang, Hongbo Yin, Zhexu Wang, Yejie Wang, Daxin Tian, Kongming Liang, Zhanyu Ma (2025-05-27T03:21:04Z). https://arxiv.org/abs/2505.20665v2

Effective autonomous driving hinges on robust reasoning across perception, prediction, planning, and behavior. However, conventional end-to-end models fail to generalize in complex scenarios due to the lack of structured reasoning. While recent vision-language models (VLMs) have been applied to driving tasks, they typically rely on isolated modules and static supervision, limiting their ability to support multi-stage decision-making. We present AutoDriveRL, a unified training framework that formulates autonomous driving as a structured reasoning process over four core tasks. Each task is independently modeled as a vision-language QA problem and optimized using task-specific reward models, enabling fine-grained reinforcement signals at different reasoning stages. Within this framework, we train DriveRX, a cross-task reasoning VLM designed for multi-stage decision-making. DriveRX achieves strong performance on the public benchmark, outperforming GPT-4o in behavior reasoning and demonstrating robustness under complex or corrupted driving conditions. DriveRX serves as a high-level semantic reasoning backbone, producing structured stage-wise reasoning chains that enhance decision consistency. These outputs also provide high-quality supervisory signals for annotation and downstream planning/control models. We release the AutoDriveRL framework and DriveRX to support future research.

- [2504.03164v2] NuScenes-SpatialQA: A Spatial Understanding and Reasoning Benchmark for Vision-Language Models in Autonomous Driving — Kexin Tian, Jingrui Mao, Yunlong Zhang, Jiwan Jiang, Yang Zhou, Zhengzhong Tu (2025-04-04T04:43:10Z). https://arxiv.org/abs/2504.03164v2

Recent advancements in Vision-Language Models (VLMs) have demonstrated strong potential for autonomous driving tasks. However, their spatial understanding and reasoning-key capabilities for autonomous driving-still exhibit significant limitations. Notably, none of the existing benchmarks systematically evaluate VLMs' spatial reasoning capabilities in driving scenarios. To fill this gap, we propose NuScenes-SpatialQA, the first large-scale ground-truth-based Question-Answer (QA) benchmark specifically designed to evaluate the spatial understanding and reasoning capabilities of VLMs in autonomous driving. Built upon the NuScenes dataset, the benchmark is constructed through an automated 3D scene graph generation pipeline and a QA generation pipeline. The benchmark systematically evaluates VLMs' performance in both spatial understanding and reasoning across multiple dimensions. Using this benchmark, we conduct extensive experiments on diverse VLMs, including both general and spatial-enhanced models, providing the first comprehensive evaluation of their spatial capabilities in autonomous driving. Surprisingly, the experimental results show that the spatial-enhanced VLM outperforms in qualitative QA but does not demonstrate competitiveness in quantitative QA. In general, VLMs still face considerable challenges in spatial understanding and reasoning.

- [2511.19912v1] Reasoning-VLA: A Fast and General Vision-Language-Action Reasoning Model for Autonomous Driving — Dapeng Zhang, Zhenlong Yuan, Zhangquan Chen, Chih-Ting Liao, Yinda Chen, Fei Shen, Qingguo Zhou, Tat-Seng Chua (2025-11-25T04:40:11Z). https://arxiv.org/abs/2511.19912v1

Vision-Language-Action (VLA) models have recently shown strong decision-making capabilities in autonomous driving. However, existing VLAs often struggle with achieving efficient inference and generalizing to novel autonomous vehicle configurations and driving scenarios. In this paper, we propose Reasoning-VLA, a general and fast action-generation VLA framework. The proposed model employs a set of learnable action queries, initialized via Gaussian sampling from ground-truth trajectories within the training corpus. These learnable queries interact with reasoning-enhanced vision-language features to generate continuous action trajectories in parallel. To promote robust generalization, we consolidate eight publicly available autonomous driving datasets into a standardized, Chain-of-Thought reasoning-based, and easy-to-use data format for model training. Leveraging both supervised learning and reinforcement learning fine-tuning, extensive empirical evaluations across multiple benchmarks demonstrate that Reasoning-VLA achieves state-of-the-art performance, superior generalization capability, and the excellent inference speed reported to date.

- [2511.22532v1] CoT4AD: A Vision-Language-Action Model with Explicit Chain-of-Thought Reasoning for Autonomous Driving — Zhaohui Wang, Tengbo Yu, Hao Tang (2025-11-27T15:13:13Z). https://arxiv.org/abs/2511.22532v1

Vision-Language-Action (VLA) models have recently attracted growing attention in end-to-end autonomous driving for their strong reasoning capabilities and rich world knowledge. However, existing VLAs often suffer from limited numerical reasoning ability and overly simplified input-output mappings, which hinder their performance in complex driving scenarios requiring step-by-step causal reasoning. To address these challenges, we propose CoT4AD, a novel VLA framework that introduces Chain-of-Thought (CoT) reasoning for autonomous driving to enhance both numerical and causal reasoning in Vision-Language Models (VLMs). CoT4AD integrates visual observations and language instructions to perform semantic reasoning, scene understanding, and trajectory planning. During training, it explicitly models a perception-question-prediction-action CoT to align the reasoning space with the action space across multiple driving tasks. During inference, it performs implicit CoT reasoning to enable consistent numerical reasoning and robust decision-making in dynamic environments. Extensive experiments on both real-world and simulated benchmarks, including nuScenes and Bench2Drive, demonstrate that CoT4AD achieves state-of-the-art performance in both open-loop and closed-loop evaluations. Code will be released upon paper acceptance.

- [2602.21952v1] MindDriver: Introducing Progressive Multimodal Reasoning for Autonomous Driving — Lingjun Zhang, Yujian Yuan, Changjie Wu, Xinyuan Chang, Xin Cai, Shuang Zeng, Linzhe Shi, Sijin Wang, Hang Zhang, Mu Xu (2026-02-25T14:34:50Z). https://arxiv.org/abs/2602.21952v1

Vision-Language Models (VLM) exhibit strong reasoning capabilities, showing promise for end-to-end autonomous driving systems. Chain-of-Thought (CoT), as VLM's widely used reasoning strategy, is facing critical challenges. Existing textual CoT has a large gap between text semantic space and trajectory physical space. Although the recent approach utilizes future image to replace text as CoT process, it lacks clear planning-oriented objective guidance to generate images with accurate scene evolution. To address these, we innovatively propose MindDriver, a progressive multimodal reasoning framework that enables VLM to imitate human-like progressive thinking for autonomous driving. MindDriver presents semantic understanding, semantic-to-physical space imagination, and physical-space trajectory planning. To achieve aligned reasoning processes in MindDriver, we develop a feedback-guided automatic data annotation pipeline to generate aligned multimodal reasoning training data. Furthermore, we develop a progressive reinforcement fine-tuning method to optimize the alignment through progressive high- level reward-based learning. MindDriver demonstrates superior performance in both nuScences open-loop and Bench2Drive closed-loop evaluation. Codes are available at https://github.com/hotdogcheesewhite/MindDriver.

- [2505.15298v4] AgentThink: A Unified Framework for Tool-Augmented Chain-of-Thought Reasoning in Vision-Language Models for Autonomous Driving — Kangan Qian, Sicong Jiang, Yang Zhong, Ziang Luo, Zilin Huang, Tianze Zhu, Kun Jiang, Mengmeng Yang, Zheng Fu, Jinyu Miao, Yining Shi, He Zhe Lim, Li Liu, Tianbao Zhou, Huang Yu, Yifei Hu, Guang Li, Guang Chen, Hao Ye, Lijun Sun, Diange Yang (2025-05-21T09:27:43Z). https://arxiv.org/abs/2505.15298v4

Vision-Language Models (VLMs) show promise for autonomous driving, yet their struggle with hallucinations, inefficient reasoning, and limited real-world validation hinders accurate perception and robust step-by-step reasoning. To overcome this, we introduce \textbf{AgentThink}, a pioneering unified framework that integrates Chain-of-Thought (CoT) reasoning with dynamic, agent-style tool invocation for autonomous driving tasks. AgentThink's core innovations include: \textbf{(i) Structured Data Generation}, which establishes an autonomous driving tool library to automatically construct structured, self-verified reasoning data explicitly incorporating tool usage for diverse driving scenarios; \textbf{(ii) A Two-stage Training Pipeline}, employing Supervised Fine-Tuning (SFT) with Group Relative Policy Optimization (GRPO) to equip VLMs with the capability for autonomous tool invocation; and \textbf{(iii) Agent-style Tool-Usage Evaluation}, introducing a novel multi-tool assessment protocol to rigorously evaluate the model's tool invocation and utilization. Experiments on the DriveLMM-o1 benchmark demonstrate that AgentThink significantly boosts overall reasoning scores by \textbf{53.91%} and enhances answer accuracy by \textbf{33.54%}, while markedly improving reasoning quality and consistency. Furthermore, ablation studies and robust zero-shot/few-shot generalization experiments across various benchmarks underscore its powerful capabilities. These findings highlight a promising trajectory for developing trustworthy and tool-aware autonomous driving models. Code is available at https://github.com/curryqka/AgentThink.

- [2508.12404v1] LMAD: Integrated End-to-End Vision-Language Model for Explainable Autonomous Driving — Nan Song, Bozhou Zhang, Xiatian Zhu, Jiankang Deng, Li Zhang (2025-08-17T15:42:54Z). https://arxiv.org/abs/2508.12404v1

Large vision-language models (VLMs) have shown promising capabilities in scene understanding, enhancing the explainability of driving behaviors and interactivity with users. Existing methods primarily fine-tune VLMs on on-board multi-view images and scene reasoning text, but this approach often lacks the holistic and nuanced scene recognition and powerful spatial awareness required for autonomous driving, especially in complex situations. To address this gap, we propose a novel vision-language framework tailored for autonomous driving, called LMAD. Our framework emulates modern end-to-end driving paradigms by incorporating comprehensive scene understanding and a task-specialized structure with VLMs. In particular, we introduce preliminary scene interaction and specialized expert adapters within the same driving task structure, which better align VLMs with autonomous driving scenarios. Furthermore, our approach is designed to be fully compatible with existing VLMs while seamlessly integrating with planning-oriented driving systems. Extensive experiments on the DriveLM and nuScenes-QA datasets demonstrate that LMAD significantly boosts the performance of existing VLMs on driving reasoning tasks,setting a new standard in explainable autonomous driving.