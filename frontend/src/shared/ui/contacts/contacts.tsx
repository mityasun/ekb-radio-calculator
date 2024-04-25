import clsx from 'clsx';
import s from './contacts.module.css';
import PhoneIcon from 'shared/assets/icon/Calling.svg?react';
import EmailIcon from 'shared/assets/icon/Message.svg?react';
import AddressIcon from 'shared/assets/icon/Map_point.svg?react';
import { PHONE, EMAIL, ADDRESS } from 'shared/constants';
import { FC } from 'react';

interface ContactsProps {
  textColor: string;
}

export const Contacts: FC<ContactsProps> = (props) => {
  const { textColor } = props;

  return (
    <div className={clsx(s.contacts)}>
      <ul className={clsx(s.contactsList)}>
        <li className={clsx(s.contactsListItem)}>
          <a
            className={clsx(s.contactsListLink)}
            href={PHONE.link}
            style={{ color: textColor }}
            target="_blank"
            rel="noreferrer">
            <PhoneIcon />
            {PHONE.title}
          </a>
        </li>
        <li className={clsx(s.contactsListItem)}>
          <a
            className={clsx(s.contactsListLink)}
            href={EMAIL.link}
            style={{ color: textColor }}
            target="_blank"
            rel="noreferrer">
            <EmailIcon />
            {EMAIL.title}
          </a>
        </li>
      </ul>
      <div className={clsx(s.address)}>
        <a href={ADDRESS.mapLink} target="_blank" rel="noreferrer">
          <AddressIcon />
        </a>
        <div>
          <p style={{ color: textColor }}>{ADDRESS.city}</p>
          <p style={{ color: textColor }}>{ADDRESS.street}</p>
        </div>
      </div>
    </div>
  );
};
