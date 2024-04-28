import clsx from 'clsx';
import s from './header.module.css';
import HeaderLogo from 'shared/assets/logo/taksa_header_logo.svg?react';
import { Contacts } from 'shared/ui/contacts';
import { Link } from 'react-router-dom';

export const Header = () => {
  return (
    <header className={clsx(s.header)}>
      <div className={clsx(s.headerWrapper)}>
        <div className={clsx(s.headerContainer)}>
          <Link to="/">
            <HeaderLogo className={clsx(s.headerIcon)} />
          </Link>
          <Contacts textColor={'#2b3140'} variant={'header'} />
        </div>
      </div>
    </header>
  );
};
