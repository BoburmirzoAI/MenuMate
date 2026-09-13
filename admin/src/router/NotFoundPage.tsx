import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';

import { Button, EmptyState } from '@shared/ui';

import { paths } from './paths';

/** 404 sahifa — mavjud emas route uchun. */
export function NotFoundPage(): JSX.Element {
  return (
    <EmptyState
      title="Sahifa topilmadi"
      description="Bu URL mavjud emas yoki o'chirilgan. Bosh sahifaga qayting."
      action={
        <Link to={paths.dashboard}>
          <Button leftIcon={<Home size={16} />}>Bosh sahifa</Button>
        </Link>
      }
    />
  );
}
