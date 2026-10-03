#![no_std]
pub mod net;
use embassy_rp::{
    bind_interrupts,
    gpio::{Input, Level, Output, Pull},
    peripherals::{DMA_CH2, DMA_CH3},
    spi,
};

use xpanse_api::{
    bus::{
        allocator::BusAllocator,
        spi::SpiBusHandle,
    },
    driver::{Driver, DriverError, DriverMeta},
    gpio_bank::{BankPins, GpioBank},
    metadata::{ModuleDetectResistor, ModuleID, ModuleSlot},
    registry::Registry,
};

pub const SPI_FREQUENCY: u32 = 30_000_000;

// Both DMA_CH2 and DMA_CH3 use DMA_IRQ_0 on the RP235x.
bind_interrupts!(pub struct Irqs {
    DMA_IRQ_0 =>
        embassy_rp::dma::InterruptHandler<DMA_CH2>,
        embassy_rp::dma::InterruptHandler<DMA_CH3>;
});

pub struct Ethernet {
    pub spi: SpiBusHandle,
    pub cs: Output<'static>,
    pub int: Input<'static>,
    pub rst: Output<'static>,
}

pub struct EthernetDriver;

impl DriverMeta for EthernetDriver {
    const ID: ModuleID = ModuleID {
        md0: ModuleDetectResistor::R1K1,
        md1: ModuleDetectResistor::R1K8,
    };
}

impl<G: BankPins> Driver<G> for EthernetDriver {
    async fn create(
        gpio_bank: GpioBank<G>,
        slot: ModuleSlot,
        registry: &mut Registry,
        bus_allocator: &mut BusAllocator,
    ) -> Result<(), DriverError> {

        let mut config = spi::Config::default();
        config.frequency = SPI_FREQUENCY;

        let spi = bus_allocator
            .create_spi_hardware::<G::SPI, DMA_CH2, DMA_CH3, _>(
                gpio_bank.gpio2, // SCK
                gpio_bank.gpio4, // MOSI
                gpio_bank.gpio3, // MISO
                Irqs,
                config,
            )
            .map_err(|_| DriverError::InitFailed)?;

        let cs = Output::new(
            gpio_bank.gpio1,
            Level::High,
        );

        let int = Input::new(
            gpio_bank.gpio5,
            Pull::Up,
        );

        let rst = Output::new(
            gpio_bank.gpio6,
            Level::High,
        );

        registry.register(
            slot,
            Self::ID,
            Ethernet {
                spi,
                cs,
                int,
                rst,
            },
        );

        Ok(())
    }
}
