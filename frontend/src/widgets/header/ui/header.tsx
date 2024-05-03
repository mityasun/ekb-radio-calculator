import clsx from 'clsx';
import s from './header.module.css';
import HeaderLogo from 'shared/assets/logo/taksa_header_logo.svg?react';
import { Contacts } from 'entities/contacts';
import { Link } from 'react-router-dom';
import { CONTACT_TEXT_COLOR } from '../configs';

export const Header = () => {
  if (window.self !== window.top) return null;

  return (
    <header className={clsx(s.header)}>
      <div className={clsx(s.headerWrapper)}>
        <div className={clsx(s.headerContainer)}>
          <Link to="/">
            <HeaderLogo className={clsx(s.headerIcon)} />
          </Link>
          <Contacts textColor={CONTACT_TEXT_COLOR.BLACK} variant={'header'} />
        </div>
      </div>
    </header>
  );
};
