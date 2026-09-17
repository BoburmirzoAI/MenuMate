import { useEffect, useState } from 'react';
import { Lock } from 'lucide-react';

import { Badge, Button, Checkbox, Input, Modal, Select, toast } from '@shared/ui';

import {
  useUpdateEndpoint,
  type EndpointAdmin,
  type PermissionAdmin,
} from './api';
import styles from './PermissionsPage.module.css';

interface Props {
  open: boolean;
  onClose: () => void;
  endpoint: EndpointAdmin | null;
  permissions: PermissionAdmin[];
}

interface State {
  access_type: EndpointAdmin['access_type'];
  permission: string;
  is_active: boolean;
  name: string;
  description: string;
}

const empty = (): State => ({
  access_type: 'authenticated',
  permission: '',
  is_active: true,
  name: '',
  description: '',
});

/** Endpoint sozlash — path va method o'zgarmaydi, faqat access_type + permission. */
export function EndpointFormModal({ open, onClose, endpoint, permissions }: Props): JSX.Element {
  const [state, setState] = useState<State>(empty());
  const update = useUpdateEndpoint();

  useEffect(() => {
    if (!open || !endpoint) return;
    const matchedPerm = permissions.find((p) => p.codename === endpoint.required_permission);
    setState({
      access_type: endpoint.access_type,
      permission: matchedPerm ? String(matchedPerm.id) : '',
      is_active: endpoint.is_active,
      name: endpoint.name ?? '',
      description: endpoint.description ?? '',
    });
  }, [open, endpoint, permissions]);

  const submit = async () => {
    if (!endpoint) return;
    const payload = {
      access_type: state.access_type,
      permission:
        state.access_type === 'permission' && state.permission
          ? Number(state.permission)
          : null,
      is_active: state.is_active,
      name: state.name.trim(),
      description: state.description.trim(),
    };
    try {
      await update.mutateAsync({ id: endpoint.id, ...payload });
      toast.success('Endpoint yangilandi', `${endpoint.method} ${endpoint.path}`);
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Saqlanmadi');
    }
  };

  if (!endpoint) return <></>;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span>
          <Lock size={16} className={styles.modalTitleIcon} />
          Endpoint sozlash
        </span>
      }
      size="md"
      footer={
        <>
          <Button variant="ghost" onClick={onClose} disabled={update.isPending}>
            Bekor
          </Button>
          <Button onClick={submit} disabled={update.isPending}>
            Saqlash
          </Button>
        </>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Badge tone="info">{endpoint.method}</Badge>
          <code style={{ fontSize: 12, color: 'var(--color-text-secondary)' }}>
            {endpoint.path}
          </code>
        </div>

        <Input
          label="Nomi"
          value={state.name}
          onChange={(e) => setState((s) => ({ ...s, name: e.target.value }))}
          placeholder="Retseptlarni ko'rish"
        />
        <Input
          label="Tavsif"
          value={state.description}
          onChange={(e) => setState((s) => ({ ...s, description: e.target.value }))}
          placeholder="Ushbu endpoint nima qiladi?"
        />

        <Select
          label="Ruxsat turi"
          value={state.access_type}
          onChange={(e) =>
            setState((s) => ({ ...s, access_type: e.target.value as State['access_type'] }))
          }
          options={[
            { label: 'Ochiq (public)', value: 'public' },
            { label: 'Autentifikatsiya (authenticated)', value: 'authenticated' },
            { label: 'Permission talab (permission)', value: 'permission' },
          ]}
        />

        {state.access_type === 'permission' && (
          <Select
            label="Kerakli permission"
            value={state.permission}
            onChange={(e) => setState((s) => ({ ...s, permission: e.target.value }))}
            options={[
              { label: '— Tanlang —', value: '' },
              ...permissions.map((p) => ({
                label: `${p.name} (${p.codename})`,
                value: String(p.id),
              })),
            ]}
          />
        )}

        <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Checkbox
            checked={state.is_active}
            onChange={(e) => setState((s) => ({ ...s, is_active: e.target.checked }))}
          />
          <span>Faol</span>
        </label>
      </div>
    </Modal>
  );
}
