import clsx from 'clsx';
import s from './adSettingsSelector.module.css';
import { AdDurationSelector } from 'entities/adDurationSelector';
import { AdMonthSelector } from 'entities/adMonthSelector';
import { AdPositionSelector } from 'entities/adPositionSelector';
import Switch from 'react-switch';
import { useAdSettingsStore } from 'shared/store';
import { Tooltip } from 'react-tooltip';
import InformationIcon from 'shared/assets/icon/information.svg?react';

const SELECT_DURATION_LABEL = 'Длительность ролика';
const SELECT_POSITION_LABEL = 'Позиционирование в рекламном блоке';
const SELECT_MONTH_LABEL = 'Месяц размешения';
const SWITCH_GUARANTEED_HOUR_LABEL = 'Гарантированный выбор часа';
const SWITCH_THIRD_PARTY_LABEL = 'Упоминание 3-их лиц';
const onColor = '#05bb75';

const DATA_TOOLTIP_TEXT = {
  SWITCH_THIRD_PARTY:
    // eslint-disable-next-line max-len
    'Выберите эту опцию, если в рекламном ролике дополнительно к вашему бренду будут задействованы также бренды других рекламодателей.',
  SWITCH_GUARANTEED_HOUR:
    // eslint-disable-next-line max-len
    'Эта опция обеспечивает выход роликов в нужный вам часовой интервал. Если не выбрать эту опцию, то радиостанция оставляет за собой право сдвинуть выходы роликов в соседние временные блоки, т.к. выбранные вами блоки могут быть уже заняты.'
};

export const AdSettingsSelector = () => {
  const { adSettings, setHourSelection, setOtherPerson } = useAdSettingsStore();

  const handleHourSelectionChange = (value: boolean) => {
    setHourSelection(value);
  };

  const handleOtherPersonChange = (value: boolean) => {
    setOtherPerson(value);
  };

  return (
    <div className={clsx(s.adSettings)}>
      <div className={clsx(s.adSettingsSelector)}>
        <div>
          <p>{SELECT_DURATION_LABEL}</p>
          <AdDurationSelector />
        </div>
        <div>
          <p>{SELECT_POSITION_LABEL}</p>
          <AdPositionSelector />
        </div>
        <div>
          <p>{SELECT_MONTH_LABEL}</p>
          <AdMonthSelector />
        </div>
      </div>
      <div className={clsx(s.adSettingsSwitch)}>
        <div>
          <p className={clsx(s.adSettingsSwitchTitle)}>
            {SWITCH_GUARANTEED_HOUR_LABEL}{' '}
            <InformationIcon
              data-tooltip-id="guaranteed-hour"
              data-tooltip-content={DATA_TOOLTIP_TEXT.SWITCH_GUARANTEED_HOUR}
            />
          </p>
          <Tooltip
            id="guaranteed-hour"
            place="bottom"
            style={{ maxWidth: '300px', backgroundColor: '#05bb75', color: '#ffffff' }}
          />
          <Switch
            onChange={handleHourSelectionChange}
            checked={adSettings.hour_selected_rate || false}
            uncheckedIcon={false}
            checkedIcon={false}
            onColor={onColor}
            activeBoxShadow="none"
          />
        </div>
        <div>
          <p className={clsx(s.adSettingsSwitchTitle)}>
            {SWITCH_THIRD_PARTY_LABEL}{' '}
            <InformationIcon
              data-tooltip-id="other-person"
              data-tooltip-content={DATA_TOOLTIP_TEXT.SWITCH_THIRD_PARTY}
            />
          </p>
          <Tooltip
            id="other-person"
            place="bottom"
            style={{ maxWidth: '300px', backgroundColor: '#05bb75', color: '#ffffff' }}
          />
          <Switch
            onChange={handleOtherPersonChange}
            checked={adSettings.other_person_rate || false}
            uncheckedIcon={false}
            checkedIcon={false}
            onColor={onColor}
            activeBoxShadow="none"
          />
        </div>
      </div>
    </div>
  );
};
