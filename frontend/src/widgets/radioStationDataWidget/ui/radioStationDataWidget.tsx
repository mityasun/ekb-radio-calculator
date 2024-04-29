import clsx from 'clsx';
import s from './radioStationDataWidget.module.css';
import { DataWidget } from 'shared/ui/dataWidget';
import ReachDlyIcon from 'shared/assets/icon/people-group-svgrepo-com.svg?react';
import LocationIcon from 'shared/assets/icon/location-svgrepo-com.svg?react';
import GenderIcon from 'shared/assets/icon/man-and-woman-svgrepo-com.svg?react';
import AudienceAgeIcon from 'shared/assets/icon/time-management-svgrepo-com.svg?react';
import { useAdSettingsStore } from 'shared/store';

const DATAWIDGET_CONTENT_TEXT = {
  BROADCAST_ZONE: 'зона вещания',
  REACH_DLY_PEOPLE_DAY: 'охват аудитории (Reach Dly)',
  REACH_DLY_PEOPLE_PRECENT: 'охват аудитории (Reach Dly)',
  AUDIENCE_SEX: 'пол аудитории',
  AUDIENCE_SEX_MEN: 'Мужчины',
  AUDIENCE_SEX_FEMAL: 'Женщины',
  AUDIENCE_AGE: 'возраст аудитории',
  AUDIENCE_CORE: 'ядро аудитории',
  UNIT_PEOPLE_DAY: ' чел./сутки',
  UNIT_PRECENT: '%',
  UNIT_UNDERFINED: '--'
};

const NUMBER_DIGIT_REGEXP = /\B(?=(\d{3})+(?!\d))/g;

export const RadioStationDataWidget = () => {
  const { selectedRadio } = useAdSettingsStore();

  if (!selectedRadio) return null;

  return (
    <div className={clsx(s.radioStationDataWidget)}>
      <DataWidget
        className={clsx(s.DataWidget1)}
        title={DATAWIDGET_CONTENT_TEXT.BROADCAST_ZONE}
        icon={<LocationIcon />}
        variant={'filled'}>
        <h4>{selectedRadio?.broadcast_zone || DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}</h4>
      </DataWidget>
      <DataWidget
        className={clsx(s.DataWidget2)}
        title={DATAWIDGET_CONTENT_TEXT.REACH_DLY_PEOPLE_DAY}
        icon={<ReachDlyIcon />}>
        <h4>
          {selectedRadio?.reach_dly
            ? selectedRadio?.reach_dly.toString().replace(NUMBER_DIGIT_REGEXP, ' ')
            : DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}
          <span>{DATAWIDGET_CONTENT_TEXT.UNIT_PEOPLE_DAY}</span>
        </h4>
      </DataWidget>
      <DataWidget
        className={clsx(s.DataWidget3)}
        title={DATAWIDGET_CONTENT_TEXT.REACH_DLY_PEOPLE_PRECENT}
        icon={<ReachDlyIcon />}>
        <h4>
          {selectedRadio?.reach_dly_percent
            ? selectedRadio?.reach_dly_percent
            : DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}
          <span>{DATAWIDGET_CONTENT_TEXT.UNIT_PRECENT}</span>
        </h4>
      </DataWidget>
      <DataWidget className={clsx(s.DataWidget4)} title={DATAWIDGET_CONTENT_TEXT.AUDIENCE_SEX} icon={<GenderIcon />}>
        <h4>
          <span>{selectedRadio?.audience_sex[1]?.sex || DATAWIDGET_CONTENT_TEXT.AUDIENCE_SEX_FEMAL} </span>
          {selectedRadio?.audience_sex[1]?.percent || DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}
          <span>{DATAWIDGET_CONTENT_TEXT.UNIT_PRECENT}</span>
        </h4>
        <h4>
          <span>{selectedRadio?.audience_sex[0]?.sex || DATAWIDGET_CONTENT_TEXT.AUDIENCE_SEX_MEN} </span>
          {selectedRadio?.audience_sex[0]?.percent || DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}
          <span>{DATAWIDGET_CONTENT_TEXT.UNIT_PRECENT}</span>
        </h4>
      </DataWidget>
      <DataWidget
        className={clsx(s.DataWidget5)}
        title={DATAWIDGET_CONTENT_TEXT.AUDIENCE_AGE}
        icon={<AudienceAgeIcon />}>
        <h4>
          <span>{DATAWIDGET_CONTENT_TEXT.AUDIENCE_CORE}</span>
          <br />
          {selectedRadio?.audience_age[0]?.age || DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}
        </h4>
        <h4>
          {selectedRadio?.audience_age[0]?.percent || DATAWIDGET_CONTENT_TEXT.UNIT_UNDERFINED}
          <span>{DATAWIDGET_CONTENT_TEXT.UNIT_PRECENT}</span>
        </h4>
      </DataWidget>
    </div>
  );
};
