import type { Plugin } from "@opencode-ai/plugin"

export const VolcengineCodingPlan: Plugin = async () => {
    return {
        config: async (cfg) => {
            const config = cfg as Record<string, any>
            config.provider["half-cabbage"] = {
                name: "半颗白菜",
                api: "https://new-api.devcxl.cn/v1/",
                npm: "@ai-sdk/openai-compatible",
                env: ["HALF_CABBAGE_API_KEY"],
                models: {
                    "glm-5.1": {
                        "id": "glm-5.1",
                        "name": "GLM-5.1",
                        "family": "glm",
                        "attachment": false,
                        "reasoning": true,
                        "reasoning_options": [
                            {
                                "type": "toggle"
                            }
                        ],
                        "tool_call": true,
                        "interleaved": {
                            "field": "reasoning_content"
                        },
                        "structured_output": true,
                        "temperature": true,
                        "release_date": "2026-03-27",
                        "last_updated": "2026-03-27",
                        "modalities": {
                            "input": [
                                "text"
                            ],
                            "output": [
                                "text"
                            ]
                        },
                        "open_weights": false,
                        "limit": {
                            "context": 200000,
                            "output": 131072
                        },
                        "cost": {
                            "input": 1.4,
                            "output": 4.4,
                            "cache_read": 0.26,
                            "cache_write": 0
                        }
                    },
                    "deepseek-v4-flash": {
                        "id": "deepseek-v4-flash",
                        "name": "DeepSeek V4 Flash",
                        "family": "deepseek-flash",
                        "attachment": false,
                        "reasoning": true,
                        "reasoning_options": [
                            {
                                "type": "toggle"
                            },
                            {
                                "type": "effort",
                                "values": [
                                    "high",
                                    "max"
                                ]
                            }
                        ],
                        "tool_call": true,
                        "interleaved": {
                            "field": "reasoning_content"
                        },
                        "structured_output": true,
                        "temperature": true,
                        "knowledge": "2025-05",
                        "release_date": "2026-04-24",
                        "last_updated": "2026-04-24",
                        "modalities": {
                            "input": [
                                "text"
                            ],
                            "output": [
                                "text"
                            ]
                        },
                        "open_weights": true,
                        "limit": {
                            "context": 1000000,
                            "output": 384000
                        },
                        "cost": {
                            "input": 0.14,
                            "output": 0.28,
                            "cache_read": 0.0028
                        }
                    },
                    "deepseek-v4-pro": {
                        "id": "deepseek-v4-pro",
                        "name": "DeepSeek V4 Pro",
                        "family": "deepseek-thinking",
                        "attachment": false,
                        "reasoning": true,
                        "reasoning_options": [
                            {
                                "type": "toggle"
                            },
                            {
                                "type": "effort",
                                "values": [
                                    "high",
                                    "max"
                                ]
                            }
                        ],
                        "tool_call": true,
                        "interleaved": {
                            "field": "reasoning_content"
                        },
                        "structured_output": true,
                        "temperature": true,
                        "knowledge": "2025-05",
                        "release_date": "2026-04-24",
                        "last_updated": "2026-04-24",
                        "modalities": {
                            "input": [
                                "text"
                            ],
                            "output": [
                                "text"
                            ]
                        },
                        "open_weights": true,
                        "limit": {
                            "context": 1000000,
                            "output": 384000
                        },
                        "cost": {
                            "input": 0.435,
                            "output": 0.87,
                            "cache_read": 0.003625
                        }
                    },
                    "minimax-m2.7": {
                        "id": "minimax-m2.7",
                        "name": "MiniMax-M2.7",
                        "family": "minimax",
                        "attachment": false,
                        "reasoning": true,
                        "reasoning_options": [],
                        "tool_call": true,
                        "temperature": true,
                        "release_date": "2026-03-18",
                        "last_updated": "2026-03-18",
                        "modalities": {
                            "input": [
                                "text"
                            ],
                            "output": [
                                "text"
                            ]
                        },
                        "open_weights": true,
                        "limit": {
                            "context": 204800,
                            "output": 131072
                        },
                        "cost": {
                            "input": 0,
                            "output": 0,
                            "cache_read": 0,
                            "cache_write": 0
                        }
                    },
                    "minimax-m3": {
                        "id": "minimax-m3",
                        "name": "MiniMax-M3",
                        "family": "minimax",
                        "attachment": true,
                        "reasoning": true,
                        "reasoning_options": [
                            {
                                "type": "toggle"
                            }
                        ],
                        "tool_call": true,
                        "temperature": true,
                        "release_date": "2026-06-01",
                        "last_updated": "2026-06-01",
                        "modalities": {
                            "input": [
                                "text",
                                "image",
                                "video"
                            ],
                            "output": [
                                "text"
                            ]
                        },
                        "open_weights": true,
                        "limit": {
                            "context": 512000,
                            "output": 128000
                        },
                        "cost": {
                            "input": 0,
                            "output": 0,
                            "cache_read": 0,
                            "cache_write": 0
                        }
                    },
                    "kimi-k2.6": {
                        "id": "kimi-k2.6",
                        "name": "Kimi K2.6",
                        "family": "kimi-k2.6",
                        "attachment": true,
                        "reasoning": true,
                        "reasoning_options": [
                            {
                                "type": "toggle"
                            }
                        ],
                        "tool_call": true,
                        "interleaved": {
                            "field": "reasoning_content"
                        },
                        "structured_output": true,
                        "temperature": true,
                        "knowledge": "2025-01",
                        "release_date": "2026-04-21",
                        "last_updated": "2026-04-21",
                        "modalities": {
                            "input": [
                                "text",
                                "image",
                                "video"
                            ],
                            "output": [
                                "text"
                            ]
                        },
                        "open_weights": true,
                        "limit": {
                            "context": 262144,
                            "output": 262144
                        },
                        "cost": {
                            "input": 0.95,
                            "output": 4,
                            "cache_read": 0.16
                        }
                    }
                }
            }
        },
    }
}
