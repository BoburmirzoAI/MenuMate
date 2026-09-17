import { useMemo, useState } from 'react';
import { Search, Shield, Users, Lock, Key, Pencil } from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  CardHeader,
  Checkbox,
  EmptyState,
  Input,
  Modal,
  PageHeader,
  Select,
  Table,
  toast,
  type TableColumn,
} from '@shared/ui';

import {
  useRoles,
  useUpdateRole,
  usePermissions,
  useEndpoints,
  type RoleAdmin,
  type PermissionAdmin,
  type EndpointAdmin,
} from './api';
import styles from './PermissionsPage.module.css';

type Tab = 'roles' | 'permissions' | 'endpoints';

const METHOD_TONE: Record<EndpointAdmin['method'], 'accent' | 'success' | 'warning' | 'info' | 'danger'> = {
  GET: 'info',
  POST: 'success',
  PATCH: 'warning',
  PUT: 'warning',
  DELETE: 'danger',
};

const ACCESS_TONE: Record<EndpointAdmin['access_type'], 'neutral' | 'accent' | 'warning'> = {
  public: 'neutral',
  authenticated: 'accent',
  permission: 'warning',
};

// Permissionni kategoriyaga bo'lish (codename.split('.')[0])
function categoryOf(perm: PermissionAdmin): string {
  return (perm.codename.split('.')[0] || 'other').replace(/^./, (c) => c.toUpperCase());
}

/** Rollar / permissionlar / endpointlar sahifasi — 3 tab. */
export function PermissionsPage(): JSX.Element {
  const [tab, setTab] = useState<Tab>('roles');
  const { data: roles = [], isLoading: rolesLoading } = useRoles();
  const { data: permissions = [], isLoading: permsLoading } = usePermissions();
  const { data: allEndpoints = [], isLoading: endpointsLoading } = useEndpoints();
  const updateRole = useUpdateRole();
  const [editingRole, setEditingRole] = useState<RoleAdmin | null>(null);

  const [rolesSearch, setRolesSearch] = useState('');
  const [permSearch, setPermSearch] = useState('');
  const [permCategory, setPermCategory] = useState<string>('all');
  const [endpointSearch, setEndpointSearch] = useState('');
  const [accessFilter, setAccessFilter] = useState<'all' | EndpointAdmin['access_type']>('all');

  const categories = useMemo(
    () => Array.from(new Set(permissions.map(categoryOf))),
    [permissions],
  );

  /** Har permission qaysi rollarga biriktirilganini hisoblab beradi. */
  const rolesByPermissionId = useMemo(() => {
    const map = new Map<number, RoleAdmin[]>();
    for (const perm of permissions) {
      map.set(perm.id, roles.filter((r) => r.permission_ids.includes(perm.id)));
    }
    return map;
  }, [roles, permissions]);

  const filteredRoles = useMemo(() => {
    const q = rolesSearch.toLowerCase().trim();
    if (!q) return roles;
    return roles.filter(
      (r) => r.name.toLowerCase().includes(q) || r.codename.toLowerCase().includes(q),
    );
  }, [roles, rolesSearch]);

  const filteredPermissions = useMemo(() => {
    const q = permSearch.toLowerCase().trim();
    return permissions.filter((p) => {
      if (permCategory !== 'all' && categoryOf(p) !== permCategory) return false;
      if (!q) return true;
      return (
        p.name.toLowerCase().includes(q) ||
        p.codename.toLowerCase().includes(q)
      );
    });
  }, [permSearch, permCategory, permissions]);

  const filteredEndpoints = useMemo(() => {
    const q = endpointSearch.toLowerCase().trim();
    return allEndpoints.filter((ep) => {
      if (accessFilter !== 'all' && ep.access_type !== accessFilter) return false;
      if (!q) return true;
      return ep.path.toLowerCase().includes(q) || ep.method.toLowerCase().includes(q);
    });
  }, [endpointSearch, accessFilter, allEndpoints]);

  const saveRolePermissions = async (roleId: number, permissionIds: number[]) => {
    try {
      await updateRole.mutateAsync({ id: roleId, permission_ids: permissionIds });
      const role = roles.find((r) => r.id === roleId);
      toast.success('Rol ruxsatlari yangilandi', `${role?.name} — ${permissionIds.length} ruxsat`);
      setEditingRole(null);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Saqlanmadi');
    }
  };

  const rolesColumns: TableColumn<RoleAdmin>[] = [
    {
      header: 'Rol',
      width: '2fr',
      cell: (r) => (
        <div className={styles.roleCell}>
          <div className={styles.roleIcon}>
            <Shield size={16} />
          </div>
          <div>
            <div className={styles.roleName}>{r.name}</div>
            <code className={styles.roleCode}>{r.codename}</code>
          </div>
        </div>
      ),
    },
    {
      header: 'Foydalanuvchilar',
      width: '1fr',
      cell: (r) => (
        <div className={styles.countCell}>
          <Users size={14} />
          <span>{r.user_count}</span>
        </div>
      ),
    },
    {
      header: 'Ruxsatlar',
      width: '1fr',
      cell: (r) => <Badge tone="accent">{r.permission_ids.length} ruxsat</Badge>,
    },
    {
      header: '',
      width: '120px',
      align: 'right',
      cell: (r) => (
        <Button
          variant="secondary"
          size="sm"
          leftIcon={<Pencil size={12} />}
          onClick={(e) => {
            e.stopPropagation();
            setEditingRole(r);
          }}
        >
          Tahrirlash
        </Button>
      ),
    },
  ];

  const permissionColumns: TableColumn<PermissionAdmin>[] = [
    {
      header: 'Nomi',
      width: '2fr',
      cell: (p) => (
        <div>
          <div className={styles.permName}>{p.name}</div>
          <code className={styles.permCode}>{p.codename}</code>
        </div>
      ),
    },
    {
      header: 'Kategoriya',
      width: '1fr',
      cell: (p) => <Badge tone="neutral">{categoryOf(p)}</Badge>,
    },
    {
      header: 'Biriktirilgan rollar',
      width: '2fr',
      cell: (p) => {
        const rolesWithPerm = rolesByPermissionId.get(p.id) ?? [];
        if (rolesWithPerm.length === 0)
          return <span className={styles.dim}>Hech biri</span>;
        return (
          <div className={styles.rolesList}>
            {rolesWithPerm.map((r) => (
              <Badge key={r.id} tone="accent">
                <Shield size={11} /> {r.name}
              </Badge>
            ))}
          </div>
        );
      },
    },
  ];

  const endpointColumns: TableColumn<EndpointAdmin>[] = [
    {
      header: 'Metod',
      width: '80px',
      cell: (ep) => <Badge tone={METHOD_TONE[ep.method]}>{ep.method}</Badge>,
    },
    {
      header: 'URL',
      width: '3fr',
      cell: (ep) => <code className={styles.pathCell}>{ep.path}</code>,
    },
    {
      header: 'Ruxsat turi',
      width: '1.2fr',
      cell: (ep) => (
        <Badge tone={ACCESS_TONE[ep.access_type]}>
          {ep.access_type === 'public'
            ? 'Ochiq'
            : ep.access_type === 'authenticated'
            ? 'Auth'
            : 'Permission'}
        </Badge>
      ),
    },
    {
      header: 'Kerakli permission',
      width: '1.5fr',
      cell: (ep) =>
        ep.required_permission ? (
          <code className={styles.permCodeSmall}>{ep.required_permission}</code>
        ) : (
          <span className={styles.dim}>—</span>
        ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Rollar va ruxsatlar"
        description={`${roles.length} rol, ${permissions.length} permission, ${allEndpoints.length} endpoint`}
      />

      <Card padded={false} className={styles.tabsCard}>
        <div className={styles.tabs}>
          <TabButton active={tab === 'roles'} onClick={() => setTab('roles')} icon={<Shield size={14} />}>
            Rollar
          </TabButton>
          <TabButton
            active={tab === 'permissions'}
            onClick={() => setTab('permissions')}
            icon={<Key size={14} />}
          >
            Permissionlar
          </TabButton>
          <TabButton
            active={tab === 'endpoints'}
            onClick={() => setTab('endpoints')}
            icon={<Lock size={14} />}
          >
            Endpoint'lar
          </TabButton>
        </div>
      </Card>

      {tab === 'roles' && (
        <>
          <Card className={styles.summaryCard}>
            <CardHeader
              title="Ruxsat tizimi"
              subtitle="Custom RBAC — foydalanuvchi rollari orqali permissionlarni oladi"
            />
            <p className={styles.explainer}>
              Har foydalanuvchi <strong>rol</strong>lar orqali <strong>permission</strong>larni oladi. Har
              endpoint DB'da yozilgan va <code>EndpointPermissionMiddleware</code> orqali tekshiriladi.
              Rolni bosib ruxsatlarini tahrirlay olasiz.
            </p>
          </Card>

          <Card padded={false} className={styles.filterCard}>
            <Input
              placeholder="Rol bo'yicha qidirish..."
              value={rolesSearch}
              onChange={(e) => setRolesSearch(e.target.value)}
              leftAdornment={<Search size={16} />}
            />
          </Card>

          <Table<RoleAdmin>
            columns={rolesColumns}
            rows={filteredRoles}
            loading={rolesLoading}
            keyExtractor={(r) => r.id}
            emptyState={<EmptyState icon={<Shield size={20} />} title="Rol topilmadi" />}
          />
        </>
      )}

      {tab === 'permissions' && (
        <>
          <Card padded={false} className={styles.filterCard}>
            <div className={styles.filters}>
              <Input
                placeholder="Permission qidirish..."
                value={permSearch}
                onChange={(e) => setPermSearch(e.target.value)}
                leftAdornment={<Search size={16} />}
              />
              <Select
                value={permCategory}
                onChange={(e) => setPermCategory(e.target.value)}
                options={[
                  { label: 'Barcha kategoriyalar', value: 'all' },
                  ...categories.map((c) => ({ label: c, value: c })),
                ]}
              />
            </div>
          </Card>

          <Table<PermissionAdmin>
            columns={permissionColumns}
            rows={filteredPermissions}
            loading={permsLoading}
            keyExtractor={(p) => p.id}
            emptyState={<EmptyState icon={<Key size={20} />} title="Permission topilmadi" />}
          />
        </>
      )}

      {tab === 'endpoints' && (
        <>
          <Card padded={false} className={styles.filterCard}>
            <div className={styles.filters}>
              <Input
                placeholder="URL yoki metod bo'yicha qidirish..."
                value={endpointSearch}
                onChange={(e) => setEndpointSearch(e.target.value)}
                leftAdornment={<Search size={16} />}
              />
              <Select
                value={accessFilter}
                onChange={(e) => setAccessFilter(e.target.value as typeof accessFilter)}
                options={[
                  { label: 'Barcha turlar', value: 'all' },
                  { label: 'Ochiq (public)', value: 'public' },
                  { label: 'Autentifikatsiya (authenticated)', value: 'authenticated' },
                  { label: 'Permission talab (permission)', value: 'permission' },
                ]}
              />
            </div>
          </Card>

          <Table<EndpointAdmin>
            columns={endpointColumns}
            rows={filteredEndpoints}
            loading={endpointsLoading}
            keyExtractor={(ep) => ep.id}
            emptyState={<EmptyState icon={<Lock size={20} />} title="Endpoint topilmadi" />}
          />
        </>
      )}

      {editingRole && (
        <RolePermissionsModal
          role={editingRole}
          permissions={permissions}
          onClose={() => setEditingRole(null)}
          onSave={(ids) => saveRolePermissions(editingRole.id, ids)}
        />
      )}
    </>
  );
}

/** Rolning permissionlarini tahrirlash modali — kategoriyalar bo'yicha checkbox'lar. */
function RolePermissionsModal({
  role,
  permissions,
  onClose,
  onSave,
}: {
  role: RoleAdmin;
  permissions: PermissionAdmin[];
  onClose: () => void;
  onSave: (permissionIds: number[]) => void;
}): JSX.Element {
  const [selected, setSelected] = useState<Set<number>>(new Set(role.permission_ids));

  const grouped = useMemo(() => {
    const map: Record<string, PermissionAdmin[]> = {};
    for (const p of permissions) {
      const cat = categoryOf(p);
      if (!map[cat]) map[cat] = [];
      map[cat]!.push(p);
    }
    return map;
  }, [permissions]);

  const toggle = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleCategory = (category: string) => {
    const catPerms = grouped[category] ?? [];
    const allSelected = catPerms.every((p) => selected.has(p.id));
    setSelected((prev) => {
      const next = new Set(prev);
      if (allSelected) catPerms.forEach((p) => next.delete(p.id));
      else catPerms.forEach((p) => next.add(p.id));
      return next;
    });
  };

  return (
    <Modal
      open
      onClose={onClose}
      title={
        <span>
          <Shield size={16} className={styles.modalTitleIcon} /> {role.name} ruxsatlari
        </span>
      }
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Bekor
          </Button>
          <Button onClick={() => onSave(Array.from(selected))}>
            Saqlash ({selected.size} ruxsat)
          </Button>
        </>
      }
    >
      <div className={styles.modalHint}>
        Ushbu rol qaysi permissionlarga ega bo'lishini tanlang. Kategoriya sarlavhasini bossangiz
        undagi hammasi bir vaqtda tanlanadi/tanlanmaydi.
      </div>

      <div className={styles.permGroups}>
        {Object.entries(grouped).map(([category, catPerms]) => {
          const selectedCount = catPerms.filter((p) => selected.has(p.id)).length;
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
                <Badge tone={selectedCount > 0 ? 'accent' : 'neutral'}>
                  {selectedCount} / {catPerms.length}
                </Badge>
              </button>
              <div className={styles.permGroupBody}>
                {catPerms.map((p) => (
                  <label key={p.id} className={styles.permRow}>
                    <Checkbox
                      checked={selected.has(p.id)}
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

function TabButton({
  active,
  onClick,
  icon,
  children,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  children: React.ReactNode;
}): JSX.Element {
  return (
    <button
      className={`${styles.tab} ${active ? styles.tabActive : ''}`}
      onClick={onClick}
      type="button"
    >
      {icon}
      {children}
    </button>
  );
}
