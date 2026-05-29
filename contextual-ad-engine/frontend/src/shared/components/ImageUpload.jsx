import { useState, useRef } from 'react';

export default function ImageUpload({ value, onChange, label = 'Upload image', accept = 'image/*' }) {
  const [preview, setPreview] = useState(value || null);
  const inputRef = useRef(null);

  function handleChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setPreview(url);
    onChange(file);
  }

  return (
    <div className="space-y-stack-xs">
      {label && <label className="text-label-md text-on-surface-variant ml-1">{label}</label>}
      <div className="grid grid-cols-2 gap-stack-md">
        {preview ? (
          <div className="aspect-square rounded-xl overflow-hidden border border-outline-variant bg-surface-container relative group">
            <img src={preview} alt="Preview" className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <button
                type="button"
                onClick={() => inputRef.current?.click()}
                className="text-white"
              >
                <span className="material-symbols-outlined">edit</span>
              </button>
            </div>
          </div>
        ) : null}
        <div
          className={`${preview ? '' : 'col-span-2'} aspect-square rounded-xl border-2 border-dashed border-outline-variant flex flex-col items-center justify-center gap-2 hover:bg-surface-container-low hover:border-primary transition-all cursor-pointer group`}
          onClick={() => inputRef.current?.click()}
        >
          <span className="material-symbols-outlined text-on-surface-variant group-hover:text-primary transition-colors text-[32px]">upload</span>
          <span className="text-label-sm text-on-surface-variant">
            {preview ? 'Replace image' : 'Click to upload'}
          </span>
        </div>
      </div>
      <input ref={inputRef} type="file" accept={accept} className="hidden" onChange={handleChange} />
    </div>
  );
}
