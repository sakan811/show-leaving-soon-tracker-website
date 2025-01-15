import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render } from '@testing-library/vue'
import CountdownTimer from '../CountdownTimer.vue'

describe('CountdownTimer', () => {
  beforeEach(() => {
    // Mock timezone-related functions
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2024-03-15T12:00:00.000Z'))
    
    // Mock timezone to ensure consistent behavior
    vi.spyOn(Intl.DateTimeFormat.prototype, 'resolvedOptions')
      .mockReturnValue({ timeZone: 'UTC' })
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('shows "Already Left" for past dates', () => {
    const { getByText } = render(CountdownTimer, {
      props: {
        date: '2024-03-14' // One day before current date
      },
      global: {
        provide: {
          userTimezone: 'UTC'
        }
      }
    })

    expect(getByText('Already Left')).toBeDefined()
  })

  it('displays countdown for future dates', async () => {
    const { container } = render(CountdownTimer, {
      props: {
        date: '2024-03-16T00:00:00.000Z' // One day after current date
      },
      global: {
        provide: {
          userTimezone: 'UTC'
        }
      }
    })

    // Run timers to trigger initial update
    await vi.runOnlyPendingTimersAsync()

    // Since we're testing exactly one day in the future at noon UTC
    // we expect 1 day 11 hours 59 minutes and 58 seconds remaining in the current day
    const countdownText = container.textContent
    expect(countdownText).toContain('1d') // 1 day since it's more than 24 hours
    expect(countdownText).toContain('11h') // 11 hours remaining
    expect(countdownText).toContain('59m') // 59 minutes remaining
    expect(countdownText).toContain('58s') // 58 seconds remaining
  })

  it('updates countdown every second', async () => {
    const { container } = render(CountdownTimer, {
      props: {
        date: '2024-03-16T00:00:00.000Z'
      },
      global: {
        provide: {
          userTimezone: 'UTC'
        }
      }
    })

    // Initial state
    await vi.runOnlyPendingTimersAsync()
    const initialText = container.textContent
    expect(initialText).toContain('h')

    // Advance time by 1 second
    await vi.advanceTimersByTimeAsync(1000)
    const updatedText = container.textContent
    
    // Verify that the countdown has changed
    expect(updatedText).not.toBe(initialText)
    expect(updatedText).toContain('h')
    expect(updatedText).toContain('m')
    expect(updatedText).toContain('s')
  })

  it('handles timezone differences correctly', async () => {
    // Set up New York timezone (UTC-5)
    const mockDate = new Date('2024-03-15T12:00:00.000-05:00')
    vi.setSystemTime(mockDate)
    
    const { container } = render(CountdownTimer, {
      props: {
        // Set target date to next day at midnight NY time
        date: '2024-03-16T05:00:00.000Z'
      },
      global: {
        provide: {
          userTimezone: 'America/New_York'
        }
      }
    })

    await vi.runOnlyPendingTimersAsync()
    
    const countdownText = container.textContent
    // Should show countdown since we're testing against NY midnight
    expect(countdownText).toMatch(/\d+[dhms]/)
    expect(countdownText).not.toBe('Already Left')
  })
})