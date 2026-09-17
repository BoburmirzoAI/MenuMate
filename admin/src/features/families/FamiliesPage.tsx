import { useState } from 'react';
import {
  UsersRound,
  MapPin,
  ChevronRight,
  Plus,
  Pencil,
  Trash2,
} from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  EmptyState,
  Modal,
  PageHeader,
  Spinner,
  toast,
} from '@shared/ui';

import {
  useFamilies,
  useFamilyDetail,
  useDeleteFamily,
  type FamilyListItem,
} from './api';
import { FamilyFormModal } from './FamilyFormModal';
import styles from './FamiliesPage.module.css';

/** Oilalar boshqaruvi sahifasi — grid + tafsilotli modal + CRUD. */
export function FamiliesPage(): JSX.Element {
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [editingFamily, setEditingFamily] = useState<FamilyListItem | null>(null);

  const { data: families = [], isLoading } = useFamilies();
  const { data: detail } = useFamilyDetail(selectedId);
  const deleteFamily = useDeleteFamily();

  const selected: FamilyListItem | null = selectedId
    ? families.find((f) => f.id === selectedId) ?? null
    : null;
  const members = detail?.members ?? [];

  const handleDelete = async (family: FamilyListItem) => {
    if (
      !window.confirm(
        `"${family.family_name}" oilasi barcha a'zolar bilan o'chiriladi. Davom etamizmi?`,
      )
    )
      return;
    try {
      await deleteFamily.mutateAsync(family.id);
      toast.info("Oila o'chirildi", family.family_name);
      setSelectedId(null);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "O'chirilmadi");
    }
  };

  return (
    <>
      <PageHeader
        title="Oilalar"
        description={
          isLoading ? 'Yuklanmoqda…' : `Ro'yxatdan o'tgan ${families.length} oila`
        }
        actions={
          <Button
            leftIcon={<Plus size={16} />}
            onClick={() => {
              setEditingFamily(null);
              setFormOpen(true);
            }}
          >
            Yangi oila
          </Button>
        }
      />

      {isLoading ? (
        <div style={{ padding: '2rem', display: 'flex', justifyContent: 'center' }}>
          <Spinner size={24} />
        </div>
      ) : families.length === 0 ? (
        <EmptyState
          icon={<UsersRound size={20} />}
          title="Hech qanday oila yo'q"
          description="Yangi oila qo'shing yoki foydalanuvchilar o'zi oila yaratishini kuting"
          action={
            <Button
              leftIcon={<Plus size={16} />}
              onClick={() => {
                setEditingFamily(null);
                setFormOpen(true);
              }}
            >
              Birinchi oila
            </Button>
          }
        />
      ) : (
        <div className={styles.grid}>
          {families.map((family) => (
            <Card
              key={family.id}
              hoverable
              onClick={() => setSelectedId(family.id)}
              className={styles.familyCard}
            >
              <div className={styles.familyHead}>
                <div className={styles.familyIcon}>
                  <UsersRound size={20} />
                </div>
                <ChevronRight size={16} className={styles.chevron} />
              </div>
              <div className={styles.familyName}>{family.family_name}</div>
              <div className={styles.familyMeta}>
                <span className={styles.metaItem}>
                  <MapPin size={12} />
                  {family.city}
                </span>
                <Badge tone="accent">{family.member_count} a'zo</Badge>
              </div>
              <div className={styles.familyDate}>
                {new Date(family.created_at).toLocaleDateString('uz-UZ')}
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal
        open={selected !== null}
        onClose={() => setSelectedId(null)}
        title={selected?.family_name}
        size="md"
        footer={
          selected && (
            <>
              <Button variant="ghost" onClick={() => setSelectedId(null)}>
                Yopish
              </Button>
              <Button
                variant="secondary"
                leftIcon={<Pencil size={16} />}
                onClick={() => {
                  setEditingFamily(selected);
                  setSelectedId(null);
                  setFormOpen(true);
                }}
              >
                Tahrirlash
              </Button>
              <Button
                variant="danger"
                leftIcon={<Trash2 size={16} />}
                onClick={() => handleDelete(selected)}
              >
                O'chirish
              </Button>
            </>
          )
        }
      >
        {selected && (
          <div className={styles.modalContent}>
            <div className={styles.modalStats}>
              <div className={styles.statBlock}>
                <div className={styles.statLabel}>Shahar</div>
                <div className={styles.statValue}>{selected.city}</div>
              </div>
              <div className={styles.statBlock}>
                <div className={styles.statLabel}>A'zolar</div>
                <div className={styles.statValue}>{selected.member_count}</div>
              </div>
              <div className={styles.statBlock}>
                <div className={styles.statLabel}>Yaratilgan</div>
                <div className={styles.statValue}>
                  {new Date(selected.created_at).toLocaleDateString('uz-UZ')}
                </div>
              </div>
            </div>

            <div className={styles.membersSection}>
              <div className={styles.membersLabel}>A'zolar</div>
              {members.length === 0 ? (
                <div className={styles.emptyHint}>Hozircha a'zolar yo'q</div>
              ) : (
                <div className={styles.membersList}>
                  {members.map((m) => (
                    <div key={m.id} className={styles.memberCard}>
                      <div className={styles.memberAvatar}>
                        {m.gender === 'FEMALE' ? '👩' : '👨'}
                      </div>
                      <div className={styles.memberInfo}>
                        <div className={styles.memberName}>
                          {m.name}{' '}
                          <span className={styles.memberAge}>· {m.age} yosh</span>
                        </div>
                        {m.health_conditions.length > 0 && (
                          <div className={styles.memberConditions}>
                            {m.health_conditions.map((hc) => (
                              <Badge key={hc.id} tone="warning">
                                {hc.name}
                              </Badge>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </Modal>

      <FamilyFormModal
        open={formOpen}
        onClose={() => setFormOpen(false)}
        family={editingFamily}
      />
    </>
  );
}
