import os

content = '''import { create } from 'zustand';

export type ElementType = 'text' | 'image' | 'shape' | 'line';

export interface EditorElement {
  id: string;
  type: ElementType;
  name: string;
  x: number; // mm
  y: number; // mm
  width: number; // mm
  height: number; // mm
  rotation: number; // degrees
  isLocked: boolean;
  
  // Text specific
  content?: string;
  fontFamily?: string;
  fontSize?: number; // px or pt, usually handled as pt. Let's use pt.
  fontWeight?: string;
  fontStyle?: string;
  textDecoration?: string;
  textAlign?: 'left' | 'center' | 'right' | 'justify';
  color?: string;
  autoFit?: boolean;
  minFontSize?: number;
  maxWidth?: number;
  
  // Image specific
  src?: string;
}

interface EditorState {
  elements: EditorElement[];
  selectedElementId: string | null;
  zoom: number; // percentage, 1 = 100%
  showGrid: boolean;
  snapToGrid: boolean;
  pageSize: { width: number; height: number }; // mm
  
  setElements: (elements: EditorElement[]) => void;
  addElement: (element: EditorElement) => void;
  updateElement: (id: string, updates: Partial<EditorElement>) => void;
  removeElement: (id: string) => void;
  setSelectedElement: (id: string | null) => void;
  setZoom: (zoom: number) => void;
  setShowGrid: (show: boolean) => void;
  setSnapToGrid: (snap: boolean) => void;
  setPageSize: (size: { width: number; height: number }) => void;
}

export const useEditorStore = create<EditorState>((set) => ({
  elements: [],
  selectedElementId: null,
  zoom: 1,
  showGrid: true,
  snapToGrid: false,
  pageSize: { width: 297, height: 210 }, // A4 Landscape by default
  
  setElements: (elements) => set({ elements }),
  addElement: (element) => set((state) => ({ elements: [...state.elements, element] })),
  updateElement: (id, updates) => set((state) => ({
    elements: state.elements.map(el => el.id === id ? { ...el, ...updates } : el)
  })),
  removeElement: (id) => set((state) => ({
    elements: state.elements.filter(el => el.id !== id),
    selectedElementId: state.selectedElementId === id ? null : state.selectedElementId
  })),
  setSelectedElement: (id) => set({ selectedElementId: id }),
  setZoom: (zoom) => set({ zoom }),
  setShowGrid: (showGrid) => set({ showGrid }),
  setSnapToGrid: (snapToGrid) => set({ snapToGrid }),
  setPageSize: (pageSize) => set({ pageSize })
}));
'''
with open('src/store/editorStore.ts', 'w', encoding='utf-8') as f:
    f.write(content)
