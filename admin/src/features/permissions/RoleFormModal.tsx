import { useEffect, useMemo, useState } from 'react';
import { Shield } from 'lucide-react';

import { Button, Checkbox, Input, Modal, toast } from '@shared/ui';

import {
  useCreateRole,
  useUpdateRole,
  type PermissionAdmin,
  type RoleAdmin,
} from './api';
import styles from './PermissionsPage.module.css';

interface Props {
  open: boolean;
  onClose: () => void;
  role: RoleAdmin | null;
  permissions: PermissionAdmin[];
}

interface State {
  name: string;
  description: string;
  is_active: boolean;
  permissionIds: Set<number>;
}

const empty = (): State => ({
  name: '',
  description: '',
  is_active: true,
  permissionIds: new Set(),
});

function categoryOf(perm: PermissionAdmin): string {
  return (perm.codename.split('.')[0] || 'other').replace(/^./, (c) => c.toUpperCase());
}

/** Rol yaratish/tahrirlash — asosiy maydonlar + permissionlar. */
export function RoleFormModal({ open, onClose, role, permissions }: Props): JSX.Element {
  const [state, setState] = useState<State>(empty());
  const create = useCreateRole();
  const update = useUpdateRole();
  const isEdit = role !== null;

  useEffect(() => {
    if (!open) return;
    if (role) {
      setState({
        name: role.name,
        description: role.description ?? '',
        is_active: role.is_active,
        permissionIds: new Set(role.permission_ids),
      });
    } else {
      setState(empty());
    }
  }, [open, role]);

  const grouped = useMemo(() => {
    const map: Record<string, PermissionAdmin[]> = {};
    for (const p of permissions) {
      const cat = categoryOf(p);
      if (!map[cat]) map[cat] = [];
      map[cat]!.push(p);
    }
    return map;
  }, [permissions]);

  const toggle = (id: number) =>
    setState((s) => {
      const next = new Set(s.permissionIds);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return { ...s, permissionIds: next };
    });

  const toggleCategory = (cat: string) => {
    const catPerms = grouped[cat] ?? [];
    const allSelected = catPerms.every((p) => state.permissionIds.has(p.id));
    setState((s) => {
      const next = new Set(s.permissionIds);
      if (allSelected) catPerms.forEach((p) => next.delete(p.id));
      else catPerms.forEach((p) => next.add(p.id));
      return { ...s, permissionIds: next };
    });
  };

  const submit = async () => {
    if (!state.name.trim()) {
      toast.error('Xatolik', 'Rol nomi majburiy');
      return;
    }
    const payload = {
      name: state.name.trim(),
      description: state.description.trim(),
      is_active: state.is_active,
      permission_ids: Array.from(state.permissionIds),
    };
    try {
      if (isEdit) {
        await update.mutateAsync({ id: role!.id, ...payload });
        toast.success('Rol yangilandi', state.name);
      } else {
        await create.mutateAsync(payload);
        toast.success('Rol yaratildi', state.name);
      }
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Saqlanmadi');
    }
  };

  const busy = create.isPending || update.isPending;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span>
          <Shield size={16} className={styles.modalTitleIcon} />
          {isEdit ? `${role!.name} tahriri` : 'Yangi rol'}
        </span>
      }
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={onClose} disabled={busy}>
            Bekor
          </Button>
          <Button onClick={submit} disabled={busy}>
            {isEdit ? 'Saqlash' : 'Yaratish'} ({state.permissionIds.size} ruxsat)
          </Button>
        </>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 16 }}>
        <Input
          label="Rol nomi *"
          value={state.name}
          onChange={(e) => setState((s) => ({ ...s, name: e.target.value }))}
          placeholder="Masalan: Moderator"
        />
        <Input
          label="Tavsif"
          value={state.description}
          onChange={(e) => setState((s) => ({ ...s, description: e.target.value }))}
          placeholder="Ushbu rol qanday vazifalarni bajaradi?"
        />
        <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Checkbox
            checked={state.is_active}
            onChange={(e) => setState((s) => ({ ...s, is_active: e.target.checked }))}
          />
          <span>Faol</span>
        </label>
      </div>

      <div className={styles.modalHint}>
        Ruxsatlarni kategoriya bo'yicha tanlang. Kategoriya sarlavhasini bosish orqali barchasini
        birdaniga tanlash/olib tashlash mumkin.
      </div>

      <div className={styles.permGroups}>
        {Object.entries(grouped).map(([category, catPerms]) => {
          const selectedCount = catPerms.filter((p) => state.permissionIds.has(p.id)).length;
          const allSelected = selectedCount === catPerms.length;
          return (
            <div key={category} className={styles.permGroup}>
              <button
                className={styles.permGroupHeader}
                onClick={() => toggleCategory(category)}
                type="button"
              >
                <Checkbox
                  checked={allSelected}
                  onChange={() => toggleCategory(category)}
                  onClick={(e) => e.stopPropagation()}
                />
                <span className={styles.permGroupName}>{category}</span>
                <span style={{ marginLeft: 'auto', fontSize: 12, color: 'var(--color-text-muted)' }}>
                  {selectedCount} / {catPerms.length}
                </span>
              </button>
              <div className={styles.permGroupBody}>
                {catPerms.map((p) => (
                  <label key={p.id} className={styles.permRow}>
                    <Checkbox
                      checked={state.permissionIds.has(p.id)}
                      onChange={() => toggle(p.id)}
                    />
                    <div className={styles.permRowText}>
                      <div className={styles.permRowName}>{p.name}</div>
                      <code className={styles.permRowCode}>{p.codename}</code>
                    </div>
                  </label>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </Modal>
  );
}
