import clsx from 'clsx';
import s from './header.module.css';
import HeaderLogo from 'shared/assets/logo/taksa_header_logo.svg?react';
import PhoneIcon from 'shared/assets/icon/Calling.svg?react';
import EmailIcon from 'shared/assets/icon/Message.svg?react';

const PHONE_NUMBER = '+7 (343) 288-72-57';
const PHONE_LINK = 'tel:+73432887257';
const EMAIL_ADDRESS = 'taksa@rataksa.ru';
const EMAIL_LINK = 'mailto:taksa@rataksa.ru';

export const Header = () => {
  return (
    <header className={clsx(s.header)}>
      <div className={clsx(s.headerWrapper)}>
        <HeaderLogo />
        <div className={clsx(s.headerContent)}>
          <ul className={clsx(s.headerContactList)}>
            <li className={clsx(s.headerContactItem)}>
              <PhoneIcon />
              <a href={PHONE_LINK}>{PHONE_NUMBER}</a>
            </li>
            <li className={clsx(s.headerContactItem)}>
              <EmailIcon />
              <a href={EMAIL_LINK}>{EMAIL_ADDRESS}</a>
            </li>
          </ul>
          <div className={clsx(s.headerAddress)}>Address</div>
        </div>
      </div>
    </header>
  );
};
