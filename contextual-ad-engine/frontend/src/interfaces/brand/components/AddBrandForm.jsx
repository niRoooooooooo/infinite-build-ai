import { useState } from 'react';
import Modal from '../../../shared/components/Modal';
import Button from '../../../shared/components/Button';
import ImageUpload from '../../../shared/components/ImageUpload';
import { createBrand } from '../../../api/brands';
import { useBrand } from '../../../context/BrandContext';

const defaultForm = {
  display_name: '',
  tagline: '',
  description: '',
  voice_tone: 'warm_casual',
  primary_color: '#00685f',
  accent_color: '#ffffff',
  secondary_color: '#888888',
};

export default function AddBrandForm({ onClose }) {
  const { refreshBrands } = useBrand();
  const [form, setForm] = useState(defaultForm);
  const [logo, setLogo] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  function set(field) {
    return (e) => setForm((prev) => ({ ...prev, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const fd = new FormData();
      Object.entries(form).forEach(([k, v]) => fd.append(k, v));
      if (logo) fd.append('logo', logo);
      await createBrand(fd);
      await refreshBrands();
      onClose();
    } catch (err) {
      setError(err.message ?? 'Failed to create brand. Please try again.');
    } finally {
      setSubmitting(false);
    }
  }

  const inputClass =
    'w-full border border-outline-variant rounded-lg px-3 py-2 text-body-md text-on-surface bg-surface-container-lowest focus:outline-none focus:border-primary transition-colors';
  const labelClass = 'block text-label-md text-on-surface-variant mb-1';

  return (
    <Modal title="Register new brand" onClose={onClose} maxWidth="max-w-[560px]">
      <form onSubmit={handleSubmit}>
        <div className="px-stack-lg py-stack-lg space-y-4 max-h-[70vh] overflow-y-auto">
          <div>
            <label className={labelClass}>Brand name *</label>
            <input
              type="text"
              required
              value={form.display_name}
              onChange={set('display_name')}
              placeholder="e.g., PRAN Foods"
              className={inputClass}
            />
          </div>

          <div>
            <label className={labelClass}>Tagline</label>
            <input
              type="text"
              value={form.tagline}
              onChange={set('tagline')}
              placeholder="e.g., Quality Always"
              className={inputClass}
            />
          </div>

          <div>
            <label className={labelClass}>Description</label>
            <textarea
              rows={3}
              value={form.description}
              onChange={set('description')}
              placeholder="Describe the brand, its audience, and what makes it unique"
              className={inputClass + ' resize-none'}
            />
          </div>

          <div>
            <label className={labelClass}>Voice / tone</label>
            <input
              type="text"
              value={form.voice_tone}
              onChange={set('voice_tone')}
              placeholder="e.g., warm_casual, bold_energetic"
              className={inputClass}
            />
          </div>

          <div className="flex gap-4">
            <div className="flex-1">
              <label className={labelClass}>Primary color</label>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={form.primary_color}
                  onChange={set('primary_color')}
                  className="h-9 w-14 rounded border border-outline-variant cursor-pointer bg-transparent"
                />
                <span className="text-body-sm text-on-surface-variant font-mono">{form.primary_color}</span>
              </div>
            </div>
            <div className="flex-1">
              <label className={labelClass}>Accent color</label>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={form.accent_color}
                  onChange={set('accent_color')}
                  className="h-9 w-14 rounded border border-outline-variant cursor-pointer bg-transparent"
                />
                <span className="text-body-sm text-on-surface-variant font-mono">{form.accent_color}</span>
              </div>
            </div>
            <div className="flex-1">
              <label className={labelClass}>Secondary color</label>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={form.secondary_color}
                  onChange={set('secondary_color')}
                  className="h-9 w-14 rounded border border-outline-variant cursor-pointer bg-transparent"
                />
                <span className="text-body-sm text-on-surface-variant font-mono">{form.secondary_color}</span>
              </div>
            </div>
          </div>

          <div>
            <label className={labelClass}>Logo</label>
            <ImageUpload onChange={setLogo} accept="image/*" label="" />
          </div>

          {error && (
            <p className="text-error text-body-sm bg-error-container/30 border border-error/20 rounded-lg px-3 py-2">
              {error}
            </p>
          )}
        </div>

        <div className="px-stack-lg py-stack-md border-t border-outline-variant flex justify-end gap-3 bg-surface-container-low">
          <Button variant="secondary" onClick={onClose} type="button">
            Cancel
          </Button>
          <Button variant="primary" type="submit" loading={submitting}>
            Create brand
          </Button>
        </div>
      </form>
    </Modal>
  );
}
