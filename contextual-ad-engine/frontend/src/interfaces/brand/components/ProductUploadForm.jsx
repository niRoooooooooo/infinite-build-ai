import { useState } from 'react';
import Modal from '../../../shared/components/Modal';
import Button from '../../../shared/components/Button';
import ImageUpload from '../../../shared/components/ImageUpload';
import { addProduct } from '../../../api/brands';

const CATEGORIES = ['beverage', 'snack', 'meal', 'grocery', 'electronics', 'fashion', 'service'];

export default function ProductUploadForm({ brandId, onSuccess, onClose }) {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!name || !category) return;
    setSubmitting(true);
    setError(null);
    try {
      const fd = new FormData();
      fd.append('name', name);
      fd.append('category', category);
      if (description) fd.append('description', description);
      if (image) fd.append('image', image);
      const newProduct = await addProduct(brandId, fd);
      onSuccess(newProduct);
      onClose();
    } catch (err) {
      setError(err.message ?? 'Upload failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  }

  const inputClass = 'w-full px-4 py-3 bg-surface-container-lowest border border-outline-variant rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all text-on-surface text-body-md';
  const labelClass = 'block text-label-md text-on-surface-variant mb-1 ml-1';

  return (
    <Modal title="Add Product" onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <div className="px-stack-lg py-stack-lg space-y-stack-md max-h-[65vh] overflow-y-auto">
          <div>
            <label className={labelClass}>Product Name *</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Pran Mango Juice 1L"
              className={inputClass}
            />
          </div>

          <div>
            <label className={labelClass}>Category *</label>
            <div className="relative">
              <select
                required
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className={inputClass + ' appearance-none cursor-pointer'}
              >
                <option value="">Select category</option>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                ))}
              </select>
              <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">
                expand_more
              </span>
            </div>
          </div>

          <div>
            <label className={labelClass}>Description</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the product, its appeal, and target audience"
              className={inputClass + ' resize-none'}
            />
          </div>

          <div>
            <label className={labelClass}>Product Image</label>
            <ImageUpload onChange={setImage} accept="image/*" label="" />
          </div>

          {error && (
            <p className="text-error text-body-sm bg-error-container/20 border border-error/20 rounded-lg px-3 py-2">
              {error}
            </p>
          )}
        </div>

        <div className="px-stack-lg py-stack-md border-t border-outline-variant flex justify-end gap-3 bg-surface-container-low">
          <Button variant="secondary" onClick={onClose} type="button">Cancel</Button>
          <Button variant="primary" type="submit" loading={submitting}>Add product</Button>
        </div>
      </form>
    </Modal>
  );
}
