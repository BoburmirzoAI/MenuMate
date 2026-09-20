import { useEffect, useRef, useState } from 'react';
import { Check, ChevronLeft, ChevronRight, ImageOff, Search, Upload } from 'lucide-react';

import { Button, toast } from '@shared/ui';

import {
  useImageSearch,
  useImageUpload,
  type ImageCandidate,
} from './api';
import styles from './RecipeImagePicker.module.css';

interface Props {
  value: string;
  onChange: (url: string) => void;
  query: string;
}

/**
 * Retsept rasmi tanlash: Wikipedia/Commons'dan qidiruv, nomzodlar o'rtasida
 * o'tish, tasdiqlash yoki lokal fayl yuklash.
 */
export function RecipeImagePicker({ value, onChange, query }: Props): JSX.Element {
  const [candidates, setCandidates] = useState<ImageCandidate[]>([]);
  const [index, setIndex] = useState(0);
  const [searched, setSearched] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const search = useImageSearch();
  const upload = useImageUpload();

  useEffect(() => {
    setCandidates([]);
    setIndex(0);
    setSearched(false);
  }, [query]);

  const doSearch = async () => {
    const q = query.trim();
    if (!q) {
      toast.error('Xatolik', 'Avval retsept nomini kiriting');
      return;
    }
    try {
      const res = await search.mutateAsync(q);
      setCandidates(res.candidates);
      setSearched(true);
      setIndex(0);
      if (res.candidates.length === 0) {
        toast.info('Hech narsa topilmadi', 'Boshqa nom bilan urinib ko\'ring');
      }
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Qidirilmadi');
    }
  };

  const doUpload = async (file: File) => {
    try {
      const res = await upload.mutateAsync(file);
      onChange(res.url);
      toast.success('Rasm yuklandi', file.name);
    } catch (err) {
      toast.error('Yuklash xatosi', err instanceof Error ? err.message : 'Xato');
    }
  };

  const onFilePick = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) doUpload(file);
    e.target.value = '';
  };

  const current = candidates[index];
  const busy = search.isPending || upload.isPending;

  return (
    <div className={styles.picker}>
      <div className={styles.previewWrap}>
        {value ? (
          <img className={styles.preview} src={value} alt="Tanlangan rasm" />
        ) : current ? (
          <img className={styles.preview} src={current.thumb_url} alt={current.title} />
        ) : (
          <div className={styles.placeholder}>
            <ImageOff size={40} />
            <span>Rasm tanlanmagan</span>
          </div>
        )}
      </div>

      {candidates.length > 0 && (
        <div className={styles.nav}>
          <button
            type="button"
            className={styles.navBtn}
            onClick={() => setIndex((i) => Math.max(0, i - 1))}
            disabled={index === 0 || busy}
            title="Oldingi"
          >
            <ChevronLeft size={18} />
          </button>
          <span className={styles.counter}>
            {index + 1} / {candidates.length}
          </span>
          <button
            type="button"
            className={styles.navBtn}
            onClick={() => setIndex((i) => Math.min(candidates.length - 1, i + 1))}
            disabled={index >= candidates.length - 1 || busy}
            title="Keyingi"
          >
            <ChevronRight size={18} />
          </button>
          <span className={styles.source}>
            {current?.source}
            {current?.lang ? ` · ${current.lang}` : ''}
          </span>
        </div>
      )}

      <div className={styles.actions}>
        {!searched && (
          <Button
            variant="secondary"
            size="sm"
            leftIcon={<Search size={14} />}
            onClick={doSearch}
            loading={search.isPending}
          >
            Wikipedia'dan qidirish
          </Button>
        )}
        {candidates.length > 0 && current && (
          <Button
            size="sm"
            leftIcon={<Check size={14} />}
            onClick={() => {
              onChange(current.thumb_url);
              toast.success('Rasm tanlandi', current.title);
            }}
            disabled={busy}
          >
            Tasdiqlash
          </Button>
        )}
        {searched && (
          <Button
            variant="ghost"
            size="sm"
            onClick={doSearch}
            loading={search.isPending}
          >
            Qayta qidirish
          </Button>
        )}
        <Button
          variant="ghost"
          size="sm"
          leftIcon={<Upload size={14} />}
          onClick={() => fileRef.current?.click()}
          loading={upload.isPending}
        >
          Rasm yuklash
        </Button>
        <input
          ref={fileRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={onFilePick}
          className={styles.hiddenFile}
        />
        {value && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onChange('')}
            disabled={busy}
          >
            Tozalash
          </Button>
        )}
      </div>
    </div>
  );
}
