import clsx from 'clsx';
import s from './modal.module.css';
import { FC, useEffect, useRef, useState } from 'react';
import ModalCloseButtonIcon from 'shared/assets/icon/modal-close-button.svg?react';

interface ModalProps {
  isOpen: boolean;
  hasCloseButton?: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const CLOSE_BUTTON_CONTENT = <ModalCloseButtonIcon />;

export const Modal: FC<ModalProps> = (props) => {
  const { isOpen, hasCloseButton, onClose, children } = props;
  const [isModalOpen, setModalOpen] = useState(isOpen);
  const modalRef = useRef<HTMLDialogElement | null>(null);

  const handleCloseModal = () => {
    if (onClose) {
      onClose();
    }
    setModalOpen(false);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDialogElement>) => {
    if (event.key === 'Escape') {
      handleCloseModal();
    }
  };

  useEffect(() => {
    setModalOpen(isOpen);
  }, [isOpen]);

  useEffect(() => {
    const modalElement = modalRef.current;

    if (modalElement) {
      if (isModalOpen) {
        modalElement.showModal();
      } else {
        modalElement.close();
      }
    }
  }, [isModalOpen]);

  return (
    <dialog ref={modalRef} onKeyDown={handleKeyDown} className={clsx(s.modal)}>
      {hasCloseButton && (
        <button className={clsx(s.modalCloseButton)} onClick={handleCloseModal}>
          {CLOSE_BUTTON_CONTENT}
        </button>
      )}
      {children}
    </dialog>
  );
};
