import { GoogleGenAI, Type, Schema } from "@google/genai";
import { SISSY_PERSONA_PROMPT, Topic, Script } from "../types";

// Ensure API key is available
const apiKey = process.env.API_KEY;

// Initialize GoogleGenAI client
// Using a fallback empty string to prevent constructor error if key is missing during initialization,
// but we check for it before making calls.
const ai = new GoogleGenAI({ apiKey: apiKey || '' });

// Using the recommended model for basic text tasks
const MODEL_NAME = "gemini-3-flash-preview";

export const generateTopics = async (input: string): Promise<Topic[]> => {
  if (!apiKey) {
    throw new Error("API Key is missing. Please check your environment variables.");
  }

  const responseSchema: Schema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        title: { type: Type.STRING, description: "The catchy title of the video topic." },
        logic: { type: Type.STRING, description: "The underlying logic or psychological insight of the topic." },
      },
      required: ["title", "logic"],
    },
  };

  try {
    const response = await ai.models.generateContent({
      model: MODEL_NAME,
      config: {
        systemInstruction: SISSY_PERSONA_PROMPT,
        responseMimeType: "application/json",
        responseSchema: responseSchema,
        temperature: 0.7,
      },
      // Simplified contents to string format as per guidelines
      contents: `请根据用户输入："${input}"，生成3个高认知、反常识的选题。`,
    });

    const text = response.text;
    if (!text) {
      throw new Error("Gemini returned an empty response.");
    }
    
    // Parse JSON
    const parsed = JSON.parse(text);
    
    if (!Array.isArray(parsed)) {
      throw new Error("Gemini response format error: expected an array.");
    }

    return parsed.map((t: any, index: number) => ({
      id: `topic-${index}`,
      title: t.title,
      logic: t.logic
    }));

  } catch (error) {
    console.error("Error generating topics:", error);
    throw error;
  }
};

export const generateScript = async (topicTitle: string, topicLogic: string): Promise<Script> => {
  if (!apiKey) {
    throw new Error("API Key is missing. Please check your environment variables.");
  }

  const responseSchema: Schema = {
    type: Type.OBJECT,
    properties: {
      hook: { type: Type.STRING, description: "黄金开头 (The Hook)" },
      attribution: { type: Type.STRING, description: "深度归因 (Deep Attribution)" },
      reversal: { type: Type.STRING, description: "认知翻转 (Cognitive Reversal)" },
      solution: { type: Type.STRING, description: "正念解题 (Mindfulness Solution)" },
      cta: { type: Type.STRING, description: "结尾与引流 (CTA)" },
    },
    required: ["hook", "attribution", "reversal", "solution", "cta"],
  };

  try {
    const response = await ai.models.generateContent({
      model: MODEL_NAME,
      config: {
        systemInstruction: SISSY_PERSONA_PROMPT,
        responseMimeType: "application/json",
        responseSchema: responseSchema,
        temperature: 0.7,
      },
      contents: `请为选题《${topicTitle}》撰写逐字稿。选题逻辑是：${topicLogic}。严格遵循5步高转化结构。`,
    });

    const text = response.text;
    if (!text) throw new Error("Gemini returned an empty response.");
    
    return JSON.parse(text) as Script;

  } catch (error) {
    console.error("Error generating script:", error);
    throw error;
  }
};
