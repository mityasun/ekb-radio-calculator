import clsx from 'clsx';
import s from './invalidSetModal.module.css';
import { FC } from 'react';
import { Modal } from 'shared/ui/modal';
import { INVALID_SET_MODAL_CONTENT_TEXT } from '../configs';
import { RadioStationSelect } from 'entities/radioStationSelect';
import { AppButton } from 'shared/ui/appButton';
import { useStore } from 'shared/store';

interface InvalidSetModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const InvalidSetModal: FC<InvalidSetModalProps> = (props) => {
  const { isOpen, onClose } = props;
  const clearCustomerSelections = useStore((state) => state.clearCustomerSelections);

  const handlerResetCustomerSelections = () => {
    clearCustomerSelections();
  };

  return (
    <Modal hasCloseButton={true} isOpen={isOpen} onClose={onClose}>
      <div className={clsx(s.invalidSetModal)}>
        <h3>{INVALID_SET_MODAL_CONTENT_TEXT.TITLE}</h3>
        <p>{INVALID_SET_MODAL_CONTENT_TEXT.TEXT}</p>
        <h4>Выбрать другую радиостанцию</h4>
        <RadioStationSelect />
        <h4>Сбросить медиаплан</h4>
        <AppButton variant={'secondary'} onClick={handlerResetCustomerSelections}>
          Сбросить медиаплан
        </AppButton>
      </div>
    </Modal>
  );
};
