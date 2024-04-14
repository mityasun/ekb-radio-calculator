import clsx from 'clsx';
import s from './header.module.css';
import HeaderLogo from 'shared/assets/logo/taksa_header_logo.svg?react';
import { Contacts } from 'shared/ui/contacts';

export const Header = () => {
  return (
    <header className={clsx(s.header)}>
      <div className={clsx(s.headerWrapper)}>
        <HeaderLogo />
        <Contacts textColor={'#2b3140'} />
      </div>
    </header>
  );
};
