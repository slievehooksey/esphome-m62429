#pragma once

#include <memory>

#include "esphome/core/component.h"
#include "esphome/core/hal.h"
#include "esphome/core/automation.h"

#include <M62429.h>

namespace esphome {
namespace m62429 {

class m62429Controller : public Component {
 public:
  void set_clk_pin(InternalGPIOPin *pin) { clk_pin_ = pin; }
  void set_dio_pin(InternalGPIOPin *pin) { dio_pin_ = pin; }
  void setup() override;
  void set_level(uint8_t volume, uint8_t channel);
  void increase(uint8_t channel = 2);
  void decrease(uint8_t channel = 2);
  void mute();
  void unmute();
  void toggle_mute();
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::HARDWARE; };

 protected:
  std::unique_ptr<M62429> volume_controller_;
  InternalGPIOPin *clk_pin_;
  InternalGPIOPin *dio_pin_;

  uint8_t level_;
  uint8_t channel_;
};

template<typename... Ts> class SetChannelLevelAction : public Action<Ts...>, public Parented<m62429Controller> {
 public:
  TEMPLATABLE_VALUE(uint8_t, level)
  TEMPLATABLE_VALUE(uint8_t, channel)

  void play(const Ts &...x) override {
    auto level = this->level_.value(x...);
    auto channel = this->channel_.value(x...);
    this->parent_->set_level(level, channel);
  }
};

template<typename... Ts> class IncreaseAction : public Action<Ts...>, public Parented<m62429Controller> {
 public:
  TEMPLATABLE_VALUE(uint8_t, channel)

  void play(const Ts &...x) override {
    auto channel = this->channel_.value(x...);
    this->parent_->increase(channel);
  }
};

template<typename... Ts> class DecreaseAction : public Action<Ts...>, public Parented<m62429Controller> {
 public:
  TEMPLATABLE_VALUE(uint8_t, channel)

  void play(const Ts &...x) override {
    auto channel = this->channel_.value(x...);
    this->parent_->decrease(channel);
  }
};

template<typename... Ts> class MuteAction : public Action<Ts...>, public Parented<m62429Controller> {
 public:
  void play(const Ts &...x) override { this->parent_->mute(); }
};

template<typename... Ts> class UnmuteAction : public Action<Ts...>, public Parented<m62429Controller> {
 public:
  void play(const Ts &...x) override { this->parent_->unmute(); }
};

template<typename... Ts> class ToggleMuteAction : public Action<Ts...>, public Parented<m62429Controller> {
 public:
  void play(const Ts &...x) override { this->parent_->toggle_mute(); }
};

}  // namespace m62429
}  // namespace esphome
