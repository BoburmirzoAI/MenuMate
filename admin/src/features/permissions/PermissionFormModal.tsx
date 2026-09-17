import { useEffect, useState } from 'react';
import { Key } from 'lucide-react';

import { Button, Input, Modal, Select, toast } from '@shared/ui';

import {
  useCreatePermission,
  useUpdatePermission,
  type PermissionAdmin,
} from './api';
import styles from './PermissionsPage.module.css';

interface Props {
  open: boolean;
  onClose: () => void;
  permission: PermissionAdmin | null;
  permissions: PermissionAdmin[];
}

interface State {
  name: string;
  codename: string;
  description: string;
  parent: string;
}

const empty = (): State => ({ name: '', codename: '', description: '', parent: '' });

/** Permission yaratish/tahrirlash — codename, name, tavsif va parent tanlash. */
export function PermissionFormModal({ open, onClose, permission, permissions }: Props): JSX.Element {
  const [state, setState] = useState<State>(empty());
  const create = useCreatePermission();
  const update = useUpdatePermission();
  const isEdit = permission !== null;

  useEffect(() => {
    if (!open) return;
    if (permission) {
      setState({
        name: permission.name,
        codename: permission.codename,
        description: permission.description ?? '',
        parent: permission.parent ? String(permission.parent) : '',
      });
    } else {
      setState(empty());
    }
  }, [open, permission]);

  const submit = async () => {
    if (!state.name.trim() || !state.codename.trim()) {
      toast.error('Xatolik', 'Nomi va codename majburiy');
      return;
    }
    const payload = {
      name: state.name.trim(),
      codename: state.codename.trim(),
      description: state.description.trim(),
      parent: state.parent ? Number(state.parent) : null,
    };
    try {
      if (isEdit) {
        await update.mutateAsync({ id: permission!.id, ...payload });
        toast.success('Permission yangilandi', state.name);
      } else {
        await create.mutateAsync(payload);
        toast.success('Permission yaratildi', state.name);
      }
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Saqlanmadi');
    }
  };

  const busy = create.isPending || update.isPending;

  const parentOptions = [
    { label: '— Parent yo\'q —', value: '' },
    ...permissions
      .filter((p) => !isEdit || p.id !== permission!.id)
      .map((p) => ({ label: `${p.name} (${p.codename})`, value: String(p.id) })),
  ];

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span>
          <Key size={16} className={styles.modalTitleIcon} />
          {isEdit ? `${permission!.name} tahriri` : 'Yangi permission'}
        </span>
      }
      size="md"
      footer={
        <>
          <Button variant="ghost" onClick={onClose} disabled={busy}>
            Bekor
          </Button>
          <Button onClick={submit} disabled={busy}>
            {isEdit ? 'Saqlash' : 'Yaratish'}
          </Button>
        </>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <Input
          label="Nomi *"
          value={state.name}
          onChange={(e) => setState((s) => ({ ...s, name: e.target.value }))}
          placeholder="Foydalanuvchilarni ko'rish"
        />
        <Input
          label="Codename *"
          value={state.codename}
          onChange={(e) => setState((s) => ({ ...s, codename: e.target.value }))}
          placeholder="users.view"
          hint="Nuqta bilan ajratilgan (masalan: users.view)"
        />
        <Input
          label="Tavsif"
          value={state.description}
          onChange={(e) => setState((s) => ({ ...s, description: e.target.value }))}
          placeholder="Ushbu ruxsat qanday harakatga ijozat beradi?"
        />
        <Select
          label="Parent permission"
          value={state.parent}
          onChange={(e) => setState((s) => ({ ...s, parent: e.target.value }))}
          options={parentOptions}
        />
      </div>
    </Modal>
  );
}
