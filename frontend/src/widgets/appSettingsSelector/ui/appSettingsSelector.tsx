import clsx from 'clsx';
import s from './appSettingsSelector.module.css';
import { DurationSelect } from 'entities/durationSelect';
import { MonthSelect } from 'entities/monthSelect';
import { PositionSelect } from 'entities/positionSelect';
import Switch from 'react-switch';
import { useStore } from 'shared/store';
import { Tooltip } from 'react-tooltip';
import InformationIcon from 'shared/assets/icon/information.svg?react';
import { AD_SETTINGS_CONTENT_TEXT, DATA_TOOLTIP_TEXT, onColor, toolTipStyle } from '../configs';

export const AppSettingsSelector = () => {
  const { appSettings, setHourSelection, setOtherPerson } = useStore();

  const handleHourSelectionChange = (value: boolean) => {
    setHourSelection(value);
  };

  const handleOtherPersonChange = (value: boolean) => {
    setOtherPerson(value);
  };

  return (
    <div className={clsx(s.appSettings)}>
      <div className={clsx(s.appSettingsSelector)}>
        <div>
          <p>{AD_SETTINGS_CONTENT_TEXT.SELECT_DURATION_LABEL}</p>
          <DurationSelect />
        </div>
        <div>
          <p>{AD_SETTINGS_CONTENT_TEXT.SELECT_POSITION_LABEL}</p>
          <PositionSelect />
        </div>
        <div>
          <p>{AD_SETTINGS_CONTENT_TEXT.SELECT_MONTH_LABEL}</p>
          <MonthSelect />
        </div>
      </div>
      <div className={clsx(s.appSettingsSwitch)}>
        <div>
          <p className={clsx(s.appSettingsSwitchTitle)}>
            {AD_SETTINGS_CONTENT_TEXT.SWITCH_HOUR_LABEL}{' '}
            <InformationIcon data-tooltip-id="guaranteed-hour" data-tooltip-content={DATA_TOOLTIP_TEXT.SWITCH_HOUR} />
          </p>
          <Tooltip id="guaranteed-hour" place="bottom" style={toolTipStyle} />
          <Switch
            onChange={handleHourSelectionChange}
            checked={appSettings.hour_selected_rate || false}
            uncheckedIcon={false}
            checkedIcon={false}
            onColor={onColor}
            activeBoxShadow="none"
          />
        </div>
        <div>
          <p className={clsx(s.appSettingsSwitchTitle)}>
            {AD_SETTINGS_CONTENT_TEXT.SWITCH_OTHER_PERSON_LABEL}{' '}
            <InformationIcon
              data-tooltip-id="other-person"
              data-tooltip-content={DATA_TOOLTIP_TEXT.SWITCH_OTHER_PERSON}
            />
          </p>
          <Tooltip id="other-person" place="bottom" style={toolTipStyle} />
          <Switch
            onChange={handleOtherPersonChange}
            checked={appSettings.other_person_rate || false}
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
